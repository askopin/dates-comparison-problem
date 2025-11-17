import manim as mn


class DrawTimeline(mn.Scene):
    def setup(self):
        self.num_ticks = 10
        self.tick_height = 0.2
        self.big_tick_height = 0.3
        self.small_tick_height = 0.15

        return super().setup()

    def create_ticks(self):
        """Create basic tick lines. Each tick represents 6 hours"""
    
        tick_marks = mn.VGroup()
        for i in range(self.num_ticks):
            x_pos = -5 + (10 * i / self.num_ticks)

            tick = mn.Line(
                start=[x_pos, -self.tick_height, 0],
                end=[x_pos, self.tick_height, 0],
                color=mn.WHITE,
                stroke_width=2,
            )

            tick_marks.add(tick)

        return tick_marks

    # Event 1 : {"id": 1, "start: 2025-12-31T18:00Z, end: 2026-01-01T06:00Z}
    # Event 2 : {"id": 2, "start: 2026-01-01T18:00Z, end: 2026-01-02T06:00Z}

    def create_task_description_objects(self):
        """Create objects for the task description section."""

        title = mn.Text("Let's assume we have two events", font_size=32).to_edge(
            mn.UP, buff=1
        )
        code_str = """
        [
          {"id": 1, "start": 2025-12-31T18:00Z, "end": 2026-01-01T06:00Z},
          {"id": 2, "start": 2026-01-01T18:00Z, "end": 2026-01-02T06:00Z}
        ]
        """
        code = mn.Code(
            code_string=code_str, language="json", add_line_numbers=False
        )
        description = mn.Paragraph(
            "We need to tell if end of the first event\nand start of the second one happens at one day",
            font_size=32,
            alignment="center",
        ).next_to(code, direction=mn.DOWN * 2)

        return title, code, description

    def create_timeline_objects(self):
        """Create objects for the timeline section."""

        timeline = mn.Arrow(
            start=mn.LEFT * 5,
            end=mn.RIGHT * 5,
            color=mn.WHITE,
            buff=0,
            stroke_width=4,
            tip_length=0.3,
        )
        tick_marks = self.create_ticks()
        timeline_text = mn.Text("Time", font_size=24).next_to(
            timeline, direction=mn.UP, aligned_edge=mn.RIGHT
        )
        first_event = mn.CubicBezier(
            4 * mn.LEFT,
            3.5 * mn.LEFT + 0.5 * mn.UP,
            2.5 * mn.LEFT + 0.5 * mn.UP,
            2 * mn.LEFT,
            stroke_color=mn.YELLOW,
        )
        first_event_text = mn.Text("First Event", font_size=22).next_to(
            first_event, direction=2 * mn.UP, aligned_edge=mn.DOWN
        )
        second_event = mn.CubicBezier(
            mn.ORIGIN,
            0.5 * mn.RIGHT + 0.5 * mn.UP,
            1.5 * mn.RIGHT + 0.5 * mn.UP,
            2 * mn.RIGHT,
            stroke_color=mn.YELLOW,
        )
        second_event_text = mn.Text("Second Event", font_size=22).next_to(
            second_event, direction=2 * mn.UP
        )

        return timeline, tick_marks, timeline_text, first_event, first_event_text, second_event, second_event_text

    def create_utc0_objects(self, tick_marks):
        """Create objects for the UTC+0 case section."""

        title = mn.Text(
            "First case: user located in London. Timezone: +0 UTC", font_size=32
        ).to_edge(mn.UP, buff=1)
        big_ben = mn.SVGMobject("big-ben.svg", fill_color=mn.WHITE, height=1).next_to(
            tick_marks[2], direction=2.2 * mn.DOWN
        )
        time_ticks = mn.VGroup(
            *[
                mn.Text(f"{(i - 2) * 6 % 24:02d}:00", font_size=22).next_to(
                    tick_marks[i], direction=mn.DOWN, aligned_edge=mn.ORIGIN
                )
                for i in range(1, self.num_ticks)
            ]
        )
        day_span = mn.Line(start=3 * mn.LEFT, end=1 * mn.RIGHT).set_stroke(
            color=mn.BLUE, width=14, opacity=0.5
        )
        day_text = mn.Text("Jan 1", font_size=22).next_to(
            tick_marks[4], direction=mn.DOWN * 3, aligned_edge=mn.ORIGIN
        )
        description = mn.MarkupText(
            '<span foreground="green" size="200%">✔︎</span> First event ends same day second one starts', font_size=30
        ).next_to(tick_marks[0], direction=mn.DOWN * 4)

        return title, big_ben, time_ticks, day_span, day_text, description

    def create_utc12_objects(self, tick_marks, timeline):
        """Create objects for the UTC+12 case section."""

        title = mn.Text(
            "Second case: user located in New Zealand. Timezone: +12 UTC", font_size=32
        ).to_edge(mn.UP, buff=1)
        kiwi = mn.SVGMobject("kiwi.svg", fill_color=mn.WHITE, height=0.8).next_to(
            tick_marks[4], direction=2.5 * mn.DOWN
        )
        time_ticks = mn.VGroup(
            *[
                mn.Text(f"{(i - 4) * 6 % 24:02d}:00", font_size=22).next_to(
                    tick_marks[i], direction=mn.DOWN, aligned_edge=mn.ORIGIN
                )
                for i in range(1, self.num_ticks)
            ]
        )
        day_0_span = mn.Line(start=5 * mn.LEFT, end=1 * mn.LEFT).set_stroke(
            color=mn.PINK, width=14, opacity=0.5
        )
        day_1_span = mn.Line(start=1 * mn.LEFT, end=3 * mn.RIGHT).set_stroke(
            color=mn.BLUE, width=14, opacity=0.5
        )
        day_0_text = mn.Text("Dec 31", font_size=22).next_to(
            tick_marks[2], direction=mn.DOWN * 3, aligned_edge=mn.ORIGIN
        )
        day_1_text = mn.Text("Jan 1", font_size=22).next_to(
            tick_marks[6], direction=mn.DOWN * 3, aligned_edge=mn.ORIGIN
        )
        description = mn.MarkupText(
            '<span foreground="red" size="200%">✘</span> First event ends the day before second one starts', font_size=30
        ).next_to(timeline, direction=mn.DOWN * 4)

        return title, kiwi, time_ticks, day_0_span, day_1_span, day_0_text, day_1_text, description

    def create_conclusion_objects(self):
        """Create objects for the conclusion section."""

        text = mn.Paragraph(
            """
                For two events in time
                there is no universal way to say
                if both happened at one day*.
            """,
            alignment="center",
            font_size=46,
        )
        note = mn.Text(
            "* Even if we ignore effects of relativity physics", font_size=22
        ).next_to(text, direction=mn.DOWN, aligned_edge=mn.RIGHT)

        return text, note

    def create_tick_animations(self, tick_marks, big_ticks=None):
        """Create tick animations with specified big tick positions.

        Args:
            tick_marks: The tick marks VGroup to animate
            big_ticks: List of indices for big ticks. If None or empty, all ticks are normalized.

        Returns:
            List of animations for the tick marks
        """
        if not big_ticks:
            # Reset all ticks to normal height
            return [tick.animate.set_length(self.tick_height) for tick in tick_marks]

        # Set specific ticks to big height, others to small height
        return [
            tick_marks[i].animate.set_length(
                self.big_tick_height if i in big_ticks else self.small_tick_height
            )
            for i in range(self.num_ticks)
        ]

    def construct(self):
        self.add_sound("sound.mp3", gain=0.3)

        # Task description section
        self.next_section("Task description")
        step_1_title, step_1_code, step_1_description = self.create_task_description_objects()

        self.add(step_1_title)
        self.play(mn.FadeIn(step_1_code))
        self.wait(1)
        self.play(mn.FadeIn(step_1_description))
        self.wait(2)
        self.play(mn.FadeOut(step_1_title, step_1_code, step_1_description))

        # Timeline section
        self.next_section("Draw a timeline")
        timeline, tick_marks, timeline_text, first_event, first_event_text, second_event, second_event_text = self.create_timeline_objects()

        self.play(mn.Create(timeline), mn.Create(tick_marks), mn.Create(timeline_text))
        self.play(mn.Create(first_event), mn.Create(first_event_text))
        self.play(mn.Create(second_event), mn.Create(second_event_text))
        self.wait(1)

        # UTC+0 case section
        self.next_section("UTC+0 case. Event 1 end and Event 2 start are at same date")
        gb_title, big_ben, gb_time_ticks, gb_day_span, gb_day_text, gb_description = self.create_utc0_objects(tick_marks)

        self.play(mn.FadeIn(gb_title))
        self.play(
            *self.create_tick_animations(tick_marks, big_ticks=[2, 6]),
            mn.Create(big_ben),
            mn.Create(gb_time_ticks),
            mn.FadeIn(gb_day_span),
            mn.Create(gb_day_text),
        )
        self.wait(1)
        self.play(mn.FadeOut(big_ben, gb_day_text))
        self.play(mn.FadeIn(gb_description))
        self.wait(1)
        self.play(
            *self.create_tick_animations(tick_marks),
            mn.FadeOut(gb_title, gb_description, gb_time_ticks, gb_day_span),
        )

        # UTC+12 case section
        self.next_section("UTC+12 case. Event 1 end and Event 2 start are at different dates")
        au_title, kiwi, au_time_ticks, au_day_0_span, au_day_1_span, au_day_0_text, au_day_1_text, au_description = self.create_utc12_objects(tick_marks, timeline)

        self.play(mn.FadeIn(au_title))
        self.play(
            *self.create_tick_animations(tick_marks, big_ticks=[4, 8]),
            mn.Create(kiwi),
            mn.Create(au_time_ticks),
            mn.FadeIn(au_day_0_span, au_day_1_span),
            mn.Create(au_day_0_text),
            mn.Create(au_day_1_text),
        )
        self.wait(1)
        self.play(mn.FadeOut(kiwi, au_day_0_text, au_day_1_text))
        self.play(mn.FadeIn(au_description))
        self.wait(2)
        
        # Fade out all MObjects for the scene
        self.play(*[mn.FadeOut(mob) for mob in self.mobjects])

        # Conclusion section
        self.next_section("Conclusion")
        conclusion_text, conclusion_note = self.create_conclusion_objects()

        self.play(mn.FadeIn(conclusion_text))
        self.wait(1)
        self.play(mn.FadeIn(conclusion_note))
        self.wait(2)
