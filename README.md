# ![icon](https://raw.githubusercontent.com/williamd1k0/redmask/master/icon.png) redmask
A simple tool to create palette swap mask


## How palette swap mask works

A palette swap mask is an image used to map a palette using a gradient scale.

The tool will generate a red gradient image because green and blue values are useless for the mask.

Full explanation about palette mask: [https://www.youtube.com/watch?v=u4Iz5AJa31Q](https://www.youtube.com/watch?v=u4Iz5AJa31Q)

![palette-mask-tuto](https://raw.githubusercontent.com/williamd1k0/redmask/master/tests/palette-mask.png)

## Using the generated mask

The mask can be used in a palette swap shader.

Example shader in Godot Engine 3.x.x:

```glsl
shader_type canvas_item;

uniform sampler2D palette;
uniform int palette_colors = 1;
uniform float color_step = 1.0;

void fragment() {
	vec4 new_color = texture(TEXTURE, UV);
	if (new_color.a > 0.0){
		vec2 palette_uv = vec2((new_color.r * 255.0) / float(palette_colors) / color_step, 0.0);
		new_color = texture(palette, palette_uv);
  }
  COLOR = new_color;
}
```

## Install

```sh
pip install redmask
```

## Basic usage

```sh
redmask <input> <palette>
# generate a mask using default color step (1)

redmask <input> <palette> -s 10
# generate a mask using 10 as color step

redmask <generated-mask> <palette> -a
# apply a palette (paint the mask) using default color step (1)
```

You can test using images in the `tests` directory.

Also, you can view usage info using the `-h/--help` command.

---

> Example art made by [Yomieda](https://twitter.com/yomieda).
