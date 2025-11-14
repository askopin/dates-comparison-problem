from manim import *

class DrawTimeline(Scene):
    def construct(self):
        timeline = Arrow(
            start=LEFT * 5,
            end=RIGHT * 5,
            color=WHITE,
            buff=0,
            stroke_width=4,
            tip_length=0.3
        )

        # Each tick represents 6 hours
        tick_marks = VGroup()
        num_ticks = 10 
        neutral_tick_height = 0.2
        big_tick_height = 0.3  
        small_tick_height = 0.15

        for i in range(num_ticks):
            x_pos = -5 + (10 * i / num_ticks)

            tick = Line(
                start=[x_pos, -neutral_tick_height, 0],
                end=[x_pos, neutral_tick_height, 0],
                color=WHITE,
                stroke_width=2
            )
            tick_marks.add(tick)
        
        timeline_text = Text("Time", font_size=24).next_to(timeline, direction = UP, aligned_edge=RIGHT)

        first_event = CubicBezier(4 * LEFT, 3.5 * LEFT + 0.5 * UP, 2.5 * LEFT + 0.5 * UP, 2 * LEFT, stroke_color=YELLOW)
        first_event_text = Text("First Event", font_size=22).next_to(first_event, direction = 2 * UP, aligned_edge=DOWN)
        second_event = CubicBezier(ORIGIN, 0.5 * RIGHT + 0.5 * UP, 1.5 * RIGHT + 0.5 * UP, 2 * RIGHT, stroke_color=YELLOW)
        second_event_text = Text("Second Event", font_size=22).next_to(second_event, direction = 2 * UP)

        self.play(Create(timeline), Create(tick_marks), Create(timeline_text))
        self.play(Create(first_event), Create(first_event_text))
        self.play(Create(second_event), Create(second_event_text))

        # Event 1 : {start: 2025-12-31T18:00Z, end: 2026-01-01T06:00Z}
        # Event 2 : {start: 2026-01-01T18:00Z, end: 2026-01-02T06:00Z}
        
        #  Drawn timeline with tick marks
        self.wait(2)
        
        self.next_section("UTC+0 case. Event 1 end and Event 2 start are at same date") 

        big_ben = SVGMobject("big-ben.svg", fill_color=WHITE, height=1).next_to(tick_marks[2], direction = 2.2 * DOWN)
        gb_zone_text = Text("Timezone: +0 UTC", font_size=22).next_to(big_ben, direction=DOWN, aligned_edge=ORIGIN)
        gb_time_ticks  = VGroup(
            *[Text(f"{ (i - 2) * 6 % 24 :02d}:00", font_size=22).next_to(tick_marks[i], direction=DOWN, aligned_edge=ORIGIN) for i in range(1, num_ticks)]
        )
 
        gb_day_span = Line(start= 3 * LEFT, end = 1 * RIGHT).set_stroke(color=BLUE, width=14, opacity=0.5)

        self.play(
            *[tick_marks[i].animate.set_length(big_tick_height if i in [2, 6] else small_tick_height) for i in range(num_ticks)], 
            Create(big_ben), Create(gb_time_ticks), Create(gb_zone_text), FadeIn(gb_day_span)
        )
        
        self.wait(2)
        
        self.next_section("UTC+12 case. Event 1 end and Event 2 start are at same date") 

        self.play(
            *[tick.animate.set_length(neutral_tick_height) for tick in tick_marks],
            FadeOut(big_ben), FadeOut(gb_time_ticks), FadeOut(gb_zone_text), FadeOut(gb_day_span)
        )
    
        kiwi = SVGMobject("kiwi.svg", fill_color=WHITE, height=0.8).next_to(tick_marks[4], direction = 2.5 * DOWN)
        au_zone_text = Text("Timezone: +12 UTC", font_size=22).next_to(kiwi, direction=DOWN, aligned_edge=ORIGIN)
        au_time_ticks = VGroup(
            *[Text(f"{ (i - 4) * 6 % 24 :02d}:00", font_size=22).next_to(tick_marks[i], direction=DOWN, aligned_edge=ORIGIN) for i in range(1, num_ticks)]
        )

        au_first_day_span = Line(start= 5 * LEFT, end = 1 * LEFT).set_stroke(color=PINK, width=14, opacity=0.5)
        au_second_day_span = Line(start= 1 * LEFT, end = 3 * RIGHT).set_stroke(color=BLUE, width=14, opacity=0.5)

        self.play(
            *[tick_marks[i].animate.set_length(big_tick_height if i in [4, 8] else small_tick_height) for i in range(num_ticks)], 
            Create(kiwi), Create(au_time_ticks), Create(au_zone_text), FadeIn(au_first_day_span), FadeIn(au_second_day_span)
        )
        self.wait(2)
