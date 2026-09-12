/*
 * Conway's Game of Life in JavaScript
 * - using the "immigration" variety
 * - and the transgender colors
 */

{
    const canvas = document.getElementById("life")
    const ctx    = canvas.getContext("2d")

    const CELL_SIZE       = 12
    const UPDATE_INTERVAL = 100

    const BLUE = 2
    const PINK = 1

    let width
    let height
    let cells
    let nextCells

    let lastUpdate = 0

    function resize()
    {
        width  = Math.ceil(window.innerWidth / CELL_SIZE)
        height = Math.ceil(window.innerHeight / CELL_SIZE)

        canvas.width  = width
        canvas.height = height

        cells     = new Uint8Array(width * height)
        nextCells = new Uint8Array(width * height)

        randomize()
    }

    // gosper's slider gun cuz idk really
    function randomize()
    {
        cells.fill(0)

        const gun = [
            [1, 5], [1, 6],
            [2, 5], [2, 6],

            [11, 5], [11, 6], [11, 7],
            [12, 4], [12, 8],
            [13, 3], [13, 9],
            [14, 3], [14, 9],
            [15, 6],
            [16, 4], [16, 8],
            [17, 5], [17, 6], [17, 7],
            [18, 6],

            [21, 3], [21, 4], [21, 5],
            [22, 3], [22, 4], [22, 5],
            [23, 2], [23, 6],
            [25, 1], [25, 2],
            [25, 6], [25, 7],

            [35, 3], [35, 4],
            [36, 3], [36, 4]
        ]

        const offsetX = 5
        const offsetY = 10

        for (const [x, y] of gun)
        {
            const gx = x + offsetX
            const gy = y + offsetY

            if (gx < 0 || gx >= width || gy < 0 || gy >= height) continue

            cells[gy * width + gx] = Math.random() < 0.5 ? BLUE : PINK
        }
    }

    function update()
    {
        let living = 0

        for (let y = 0; y < height; y++)
        {
            for (let x = 0; x < width; x++)
            {
                const i = y * width + x

                let neighbors = 0, blue = 0, pink = 0

                for (let dy = -1; dy <= 1; dy++)
                {
                    for (let dx = -1; dx <= 1; dx++)
                    {
                        if (dx === 0 && dy === 0) continue
                        
                        const neighbor = cells[((y + dy + height) % height) * width + (x + dx + width) % width]
                        
                        if (neighbor) 
                        {
                            neighbors++
                            
                            if (neighbor === BLUE) blue++
                            else pink++
                        }
                    }
                }

                if (cells[i]) nextCells[i] = (neighbors === 2 || neighbors === 3) ? cells[i] : 0
                else if (neighbors === 3) nextCells[i] = blue > pink ? BLUE : pink > blue ? PINK : (Math.random() < 0.5 ? BLUE : PINK)
                else nextCells[i] = 0

                if (nextCells[i]) living++
            }
        }

        ;[cells, nextCells] = [nextCells, cells]

        // if (living < 5) randomize() // useless lol
    }

    function draw()
    {
        ctx.clearRect(0, 0, width, height)
        
        for (let i = 0; i < cells.length; i++)
        {
            if (!cells[i]) continue
            
            ctx.fillStyle = cells[i] === BLUE ? "#c3e0ec" : "#ecd6da"
            
            ctx.fillRect(i % width, Math.floor(i / width), 1, 1)
        }
    }

    function animate(time)
    {
        // because chroMEMEmium, so
        if (!document.hidden && time - lastUpdate >= UPDATE_INTERVAL) 
        {
            update()
            draw()
            
            lastUpdate = time
        }
        
        requestAnimationFrame(animate)
    }

    window.addEventListener("resize", resize)
    
    resize()
    draw()
    requestAnimationFrame(animate)
}
