import gg
import gx
import math

const (
	box_size = 73  // Size of tile grid
	app_size = 1010 // Size of app window
)

struct SandPile {
	pub:
		size int
	pub mut:
		grid [][]int
}

fn (pile SandPile) print(){
	for row in pile.grid {
		for element in row {
			print('${element} ')
		}
		print('\n')
	}
}

fn (mut pile SandPile) update(){
	mut grid_copy := pile.grid.clone()

	for y in 0..pile.size {
		for x in 0..pile.size {
			if pile.grid[y][x] >= 4 {
				if y - 1 >= 0             {grid_copy[y - 1][x] += 1}
				if y + 1 <= pile.size - 1 {grid_copy[y + 1][x] += 1}
				if x - 1 >= 0             {grid_copy[y][x - 1] += 1}
				if x + 1 <= pile.size -1  {grid_copy[y][x + 1] += 1}

				grid_copy[y][x]     -= 4
			}
		}
	}

	pile.grid = grid_copy
}

fn new_pile(size int) &SandPile{
	grid := [][]int{len: size, init: []int{len: size, init: 0}}
	return &SandPile{size: size, grid: grid}
}

struct App {
	pub mut:
		gg &gg.Context
		pile &SandPile
}

fn main() {
	mut app := &App{
		gg: &gg.Context{}
		pile: &SandPile{}
	}

	app.pile = new_pile(box_size)

	app.pile.grid[36][36] = 10000

	app.gg = gg.new_context(
		bg_color: gx.rgb(174, 198, 255),
		width: app_size,
		height: app_size,
		window_title: 'Sand Piles',
		frame_fn: frame,
		user_data: app,
		keydown_fn: key_down,
		fullscreen: true, 
	)

	app.gg.run()
	
}



fn frame(mut app App) {
	app.gg.begin()
	tile_size := app_size / app.pile.size
	text_cfg := gx.TextCfg{
		color: gx.rgb(255, 255, 255),
		align: .center,
		vertical_align: .middle,
		size: tile_size / 4,
	}

	for y in 0..app.pile.size{
		for x in 0..app.pile.size{
			n := app.pile.grid[y][x]
			r := 255 * math.atan(f32(n) / 6.5)

			mut color:= gx.rgb(0, 0, 0)
			if n >= 4 {
				color = gx.rgb(255, 255, 55)
			} else {
				color = gx.rgb(u8(r), u8(r), 0)
			}

			app.gg.draw_rect_filled(x * tile_size,  y       * tile_size, tile_size, tile_size, color)
			app.gg.draw_text(
				int(x * tile_size + tile_size / 2),
				int(y * tile_size + tile_size / 2),
				'${n}',
				text_cfg,
			)
		}
	}

	app.gg.end()
}

fn key_down(c gg.KeyCode, m gg.Modifier, mut app App){
	match c {
		.escape { exit(0) }
		else {
			app.pile.update()
		}
	}
}