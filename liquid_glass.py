import inkex
import math
from lxml import etree

etree.register_namespace('xlink', 'http://www.w3.org/1999/xlink')

INKSCAPE_NS = 'http://www.inkscape.org/namespaces/inkscape'

class LiquidGlassExtension(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--tabs", type=str, default="", help="Ignorar parâmetro de abas")

        pars.add_argument("--bg_id", type=str, default="")
        pars.add_argument("--normal-map_offset", type=float, default=0.1)
        pars.add_argument("--normal-map_softness", type=float, default=0.1)
        pars.add_argument("--displacement_map", type=float, default=0.1)
        pars.add_argument("--glass_blur", type=float, default=0.1)

        pars.add_argument("--highlight_angle", type=float, default=45.0)
        pars.add_argument("--highlight_intensity", type=float, default=0.5)
        pars.add_argument("--highlight_softness", type=float, default=0.5)
        pars.add_argument("--highlight_size", type=float, default=0.5)
        pars.add_argument("--inner_shadow_opacity", type=float, default=0.5)
        pars.add_argument("--inner_shadow_blur", type=float, default=0.5)
        pars.add_argument("--inner_shadow_offset", type=float, default=0.1)

        pars.add_argument("--bg_color", type=str, default="#ffffff00")
        
        pars.add_argument("--drop_shadow_color", type=str, default="#00000000")
        pars.add_argument("--drop_shadow_blur", type=float, default=0.5)
        pars.add_argument("--drop_shadow_offset_x", type=float, default=0.1)
        pars.add_argument("--drop_shadow_offset_y", type=float, default=0.1)

    # Convert an integer color value to a hex color string       
    def int_to_hex_color(self, color_int):
        red   = (color_int >> 24) & 0xFF  
        green = (color_int >> 16) & 0xFF  
        blue  = (color_int >> 8)  & 0xFF  
        alpha = color_int & 0xFF          
        return f"#{red:02x}{green:02x}{blue:02x}{alpha:02x}"

    def effect(self):
        bg = self.options.bg_id
        nm_offset = self.options.normal_map_offset
        nm_softness = self.options.normal_map_softness
        displacement = self.options.displacement_map
        glass_blur = self.options.glass_blur

        highlight_angle = self.options.highlight_angle
        highlight_intensity = self.options.highlight_intensity
        highlight_softness = self.options.highlight_softness
        highlight_size = self.options.highlight_size
        inner_shadow_opacity = self.options.inner_shadow_opacity
        inner_shadow_blur = self.options.inner_shadow_blur
        inner_shadow_offset = self.options.inner_shadow_offset

        bg_color = self.int_to_hex_color(int(self.options.bg_color))

        drop_shadow_color = self.int_to_hex_color(int(self.options.drop_shadow_color))
        drop_shadow_blur = self.options.drop_shadow_blur
        drop_shadow_offset_x = self.options.drop_shadow_offset_x
        drop_shadow_offset_y = self.options.drop_shadow_offset_y

        # Validate the background image

        if not bg:
            inkex.errormsg("Please select a background image for the liquid glass effect.")
            return

        # Create the filter definition
        if not self.svg.selection:
            inkex.errormsg("Please select at least one object to apply the liquid glass effect.")
            return

        # Create the filter in the SVG document

        svg = self.document.getroot()
        defs = svg.find('{http://www.w3.org/2000/svg}defs')
        if defs is None:
            defs = etree.SubElement(svg, 'defs')

        ns_xlink = "http://www.w3.org/1999/xlink"

        for elem in self.svg.selection:
            f_id = self.svg.get_unique_id('liquid_glass')
            f = etree.SubElement(defs, 'filter', {
                'style': 'color-interpolation-filters:sRGB',
                'id': f_id,
                'x': '-0.035728916',
                'y': '-0.21407224',
                'width': '1.0714578',
                'height': '1.4281445'
            })

            f.set(f'{{{INKSCAPE_NS}}}label', 'Liquid Glass V2.0')

            # Normal Map
            etree.SubElement(f, 'feFlood', {
                'id': 'feFlood1',
                'flood-color': 'rgb(128, 0, 128)',
                'flood-opacity': '1.0',
                'result': 'result1'
            })
            etree.SubElement(f, 'feFlood', {
                'in': 'SourceGraphic',
                'id': 'feFlood2',
                'flood-color': 'rgb(128, 0, 0)',
                'flood-opacity': '0.5',
                'result': 'result2'
            })
            etree.SubElement(f, 'feOffset', {
                'id': 'feOffset1',
                'dx':  str(nm_offset*-1),
                'dy': '0',
                'in': 'SourceGraphic',
                'result': 'result3'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite1',
                'operator': 'out',
                'in': 'result2',
                'in2': 'result3',
                'result': 'result4'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite2',
                'operator': 'atop',
                'in': 'result4',
                'in2': 'result1',
                'result': 'result4'
            })
            etree.SubElement(f, 'feFlood', {
                'in': 'SourceGraphic',
                'id': 'feFlood3',
                'flood-color': 'rgb(128, 0, 255)',
                'flood-opacity': '0.5',
                'result': 'result5'
            })
            etree.SubElement(f, 'feOffset', {
                'id': 'feOffset2',
                'dx': str(nm_offset),
                'dy': '0',
                'in': 'SourceGraphic',
                'result': 'result6'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite3',
                'operator': 'out',
                'in': 'result5',
                'in2': 'result6',
                'result': 'result7'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite4',
                'operator': 'atop',
                'in': 'result7',
                'in2': 'result4',
                'result': 'result8'
            })
            etree.SubElement(f, 'feFlood', {
                'in': 'SourceGraphic',
                'id': 'feFlood4',
                'flood-color': 'rgb(0, 0, 128)',
                'flood-opacity': '0.5',
                'result': 'result9'
            })
            etree.SubElement(f, 'feOffset', {
                'id': 'feOffset3',
                'dx': '0',
                'dy': str(nm_offset*-1),
                'in': 'SourceGraphic',
                'result': 'result10'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite5',
                'operator': 'out',
                'in': 'result9',
                'in2': 'result10',
                'result': 'result11'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite6',
                'operator': 'atop',
                'in': 'result11',
                'in2': 'result8',
                'result': 'result12'
            })
            etree.SubElement(f, 'feFlood', {
                'in': 'SourceGraphic',
                'id': 'feFlood5',
                'flood-color': 'rgb(255, 0, 128)',
                'flood-opacity': '0.5',
                'result': 'result13'
            })
            etree.SubElement(f, 'feOffset', {
                'id': 'feOffset4',
                'dx': '0',
                'dy': str(nm_offset),
                'in': 'SourceGraphic',
                'result': 'result14'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite7',
                'operator': 'out',
                'in': 'result13',
                'in2': 'result14',
                'result': 'result15'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite8',
                'operator': 'atop',
                'in': 'result15',
                'in2': 'result12',
                'result': 'result16'
            })
            etree.SubElement(f, 'feGaussianBlur', {
                'id': 'feGaussianBlur1',
                'stdDeviation': str(nm_softness),
                'in': 'result16',
                'result': 'result17'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite9',
                'operator': 'in',
                'in': 'result17',
                'in2': 'SourceGraphic',
                'result': 'result18'
            })

            # Displacement Map
            etree.SubElement(f, 'feImage', {
                'id': 'feImage1',
                etree.QName(ns_xlink, 'href'): f"#{bg}",
                'x': '0',
                'y': '0',
                'result': 'result19',
            })
            etree.SubElement(f, 'feDisplacementMap', {
                'id': 'feDisplacementMap1',
                'in': 'result19',
                'in2': 'result18',
                'scale': str(displacement),
                'xChannelSelector': 'B',
                'yChannelSelector': 'R',
                'result': 'result20'
            })
            etree.SubElement(f, 'feGaussianBlur', {
                'id': 'feGaussianBlur2',
                'stdDeviation': str(glass_blur),
                'in': 'result20',
                'result': 'result21'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite10',
                'operator': 'in',
                'in': 'result21',
                'in2': 'SourceGraphic',
                'result': 'result22'
            })

            #highlight
            highlight_angle_rad = highlight_angle * (3.141592653589793 / 180.0)
            highlight_dx = highlight_size * math.cos(highlight_angle_rad)
            highlight_dy = highlight_size * math.sin(highlight_angle_rad)

            etree.SubElement(f, 'feFlood', {
                'id': 'feFlood6',
                'flood-color': f'rgb(255, {int(255 * highlight_intensity)}, {int(255 * highlight_intensity)})',
                'flood-opacity': str(highlight_intensity / 100),
                'result': 'result23'
            })
            etree.SubElement(f, 'feOffset', {
                'id': 'feOffset5',
                'dx': str(highlight_dx),
                'dy': str(highlight_dy),
                'in': 'SourceGraphic',
                'result': 'result24'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite11',
                'operator': 'out',
                'in': 'result23',
                'in2': 'result24',
                'result': 'result25'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite12',
                'operator': 'in',
                'in': 'result25',
                'in2': 'SourceGraphic',
                'result': 'result26'
            })
            etree.SubElement(f, 'feOffset', {
                'id': 'feOffset6',
                'dx': str((highlight_dx * -1) * 0.6),
                'dy': str((highlight_dy * -1) * 0.6),
                'in': 'SourceGraphic',
                'result': 'result27'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite13',
                'operator': 'out',
                'in': 'result23',
                'in2': 'result27',
                'result': 'result28'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite14',
                'operator': 'in',
                'in': 'result28',
                'in2': 'SourceGraphic',
                'result': 'result29'
            })

            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite15',
                'operator': 'over',
                'in': 'result26',
                'in2': 'result29',
                'result': 'result30'
            })

            etree.SubElement(f, 'feGaussianBlur', {
                'id': 'feGaussianBlur3',
                'stdDeviation': str(highlight_softness),
                'in': 'result30',
                'result': 'result31'
            })

            #inner shadow
            etree.SubElement(f, 'feFlood', {
                'id': 'feFlood7',
                'flood-color': 'rgb(0, 0, 0)',
                'flood-opacity': str(inner_shadow_opacity / 100),
                'result': 'result32'
            })
            etree.SubElement(f, 'feOffset', {
                'id': 'feOffset7',
                'dx': '0',
                'dy': str(inner_shadow_offset),
                'in': 'SourceGraphic',
                'result': 'result33'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite15',
                'operator': 'out',
                'in': 'result32',
                'in2': 'result33',
                'result': 'result34'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite16',
                'operator': 'in',
                'in': 'result34',
                'in2': 'SourceGraphic',
                'result': 'result35'
            })
            etree.SubElement(f, 'feGaussianBlur', {
                'id': 'feGaussianBlur4',
                'stdDeviation': str(inner_shadow_blur),
                'in': 'result35',
                'result': 'result36'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite17',
                'operator': 'in',
                'in': 'result36',
                'in2': 'SourceGraphic',
                'result': 'result37'
            })

            # glass composite
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite18',
                'operator': 'over',
                'in': 'result31',
                'in2': 'result37',
                'result': 'result38'
            })

            #background color

            # Check if the background color is set
            bg_color_hex = bg_color if bg_color.startswith('#') else f'#{bg_color}'
            bg_color_opacity = 1.0
            if len(bg_color_hex) == 9:
                bg_color_opacity = int(bg_color_hex[7:9], 16) / 255.0
                bg_color_hex = bg_color_hex[:7] 

            # Create background color filter
            etree.SubElement(f, 'feFlood', {
                'id': 'feFlood8',
                'flood-color': str(bg_color_hex),
                'flood-opacity': str(bg_color_opacity),
                'result': 'result40'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite20',
                'operator': 'atop',
                'in': 'result40',
                'in2': 'result22',
                'result': 'result41'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite21',
                'operator': 'atop',
                'in': 'result38',
                'in2': 'result41',
                'result': 'result42'
            })

            #drop shadow
            drop_shadow_color_hex = drop_shadow_color if drop_shadow_color.startswith('#') else f'#{drop_shadow_color}'
            drop_shadow_opacity = 1.0
            if len(drop_shadow_color_hex) == 9:
                drop_shadow_opacity = int(drop_shadow_color_hex[7:9], 16) / 255.0
                drop_shadow_color_hex = drop_shadow_color_hex[:7]

            etree.SubElement(f, 'feFlood', {
                'id': 'feFlood9',
                'flood-color': str(drop_shadow_color_hex),
                'flood-opacity': str(drop_shadow_opacity),
                'result': 'result43'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite22',
                'operator': 'in',
                'in': 'result43',
                'in2': 'SourceGraphic',
                'result': 'result44'
            })
            etree.SubElement(f, 'feGaussianBlur', {
                'id': 'feGaussianBlur6',
                'stdDeviation': str(drop_shadow_blur),
                'in': 'result44',
                'result': 'result45'
            })
            etree.SubElement(f, 'feOffset', {
                'id': 'feOffset8',
                'dx': str(drop_shadow_offset_x),
                'dy': str(drop_shadow_offset_y),
                'in': 'result45',
                'result': 'result46'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite23',
                'operator': 'out',
                'in': 'result46',
                'in2': 'SourceGraphic',
                'result': 'result47'
            })
            etree.SubElement(f, 'feComposite', {
                'id': 'feComposite24',
                'operator': 'over',
                'in': 'result47',
                'in2': 'result42',
                'result': 'result48'
            })

            style = elem.style
            style['filter'] = f'url(#{f_id})'
            elem.set('style', style.to_str())

if __name__ == '__main__':
    LiquidGlassExtension().run()
