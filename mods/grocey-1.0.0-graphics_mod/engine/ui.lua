UIElement.draw_pixellated_rect = nil
UIElement.draw_pixellated_rect = function(self, _type, _parallax, _emboss, _progress)
    if not self.pixellated_rect or #self.pixellated_rect[_type].vertices < 1 or _parallax ~=
        self.pixellated_rect.parallax or self.pixellated_rect.w ~= self.VT.w or self.pixellated_rect.h ~= self.VT.h or
        self.pixellated_rect.sw ~= self.shadow_parrallax.x or self.pixellated_rect.sh ~= self.shadow_parrallax.y or
        self.pixellated_rect.progress ~= (_progress or 1) then
        self.pixellated_rect = {
            w = self.VT.w,
            h = self.VT.h,
            sw = self.shadow_parrallax.x,
            sh = self.shadow_parrallax.y,
            progress = (_progress or 1),
            fill = {
                vertices = {}
            },
            shadow = {
                vertices = {}
            },
            line = {
                vertices = {}
            },
            emboss = {
                vertices = {}
            },
            line_emboss = {
                vertices = {}
            },
            parallax = _parallax
        }
        local ext_up = self.config.ext_up and self.config.ext_up * G.TILESIZE or 0
        local res = self.config.res or math.min(self.VT.w, self.VT.h + math.abs(ext_up) / G.TILESIZE) > 3.5 and 0.8 or
                        math.min(self.VT.w, self.VT.h + math.abs(ext_up) / G.TILESIZE) > 0.3 and 0.6 or 0.15
        local totw, toth = self.VT.w * G.TILESIZE, (self.VT.h + math.abs(ext_up) / G.TILESIZE) * G.TILESIZE

        -- Set up coordinates for our rounded rectangle approximation:
        local x = 0
        local y = 0 - ext_up -- shift upward by ext_up as in the original
        local radius = 4 * res -- adjust this value for more or less rounding

        -- Hard-coded octagon vertices approximating a rounded rectangle
        local vertices = {x + radius, y, -- top edge start (inset from left)
        x + totw - radius, y, -- top edge end (inset from right)
        x + totw, y + radius, -- right edge, top curve start
        x + totw, y + toth - radius, -- right edge, bottom curve end
        x + totw - radius, y + toth, -- bottom edge end (inset from right)
        x + radius, y + toth, -- bottom edge start (inset from left)
        x, y + toth - radius, -- left edge, bottom curve start
        x, y + radius -- left edge, top curve end
        }

        for k, v in ipairs(vertices) do
            if k % 2 == 1 and v > totw * self.pixellated_rect.progress then
                v = totw * self.pixellated_rect.progress
            end
            self.pixellated_rect.fill.vertices[k] = v
            self.pixellated_rect.line.vertices[k] = v
            if _emboss then
                self.pixellated_rect.line_emboss.vertices[k] = v +
                                                                   (k % 2 == 0 and -_emboss * self.shadow_parrallax.y or
                                                                       -0.7 * _emboss * self.shadow_parrallax.x)
            end
            if k % 2 == 0 then
                self.pixellated_rect.shadow.vertices[k] = v - self.shadow_parrallax.y * _parallax
                if _emboss then
                    self.pixellated_rect.emboss.vertices[k] = v + _emboss * G.TILESIZE
                end
            else
                self.pixellated_rect.shadow.vertices[k] = v - self.shadow_parrallax.x * _parallax
                if _emboss then
                    self.pixellated_rect.emboss.vertices[k] = v
                end
            end
        end
    end

    love.graphics.polygon((_type == 'line' or _type == 'line_emboss') and 'line' or 'fill',
        self.pixellated_rect[_type].vertices)
end
