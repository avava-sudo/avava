from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class BinaryCalc(App):
    def build(self):
        self.from_base = 2  # По умолчанию сразу 2-ичная
        
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=8)
        
        # 1. Поле ввода
        self.input_num = TextInput(
            text='', 
            hint_text='Введите число (напр. 1101101)', 
            multiline=False, 
            font_size=20,
            size_hint_y=0.1
        )
        main_layout.add_widget(self.input_num)
        
        # 2. Выбор ИСХОДНОЙ системы счисления
        lbl_from = Label(text='Исходная система числа (ИЗ):', font_size=14, size_hint_y=0.05, color=(0.7, 0.7, 0.7, 1))
        main_layout.add_widget(lbl_from)
        
        from_layout = BoxLayout(orientation='horizontal', spacing=5, size_hint_y=0.08)
        self.from_buttons = {}
        bases = [('Из 2', 2), ('Из 8', 8), ('Из 10', 10), ('Из 16', 16)]
        
        for text, b in bases:
            btn = Button(
                text=text, 
                font_size=14, 
                background_color=(0.2, 0.6, 1, 1) if b == 2 else (0.3, 0.3, 0.3, 1)
            )
            btn.bind(on_press=lambda x, base=b: self.set_from_base(base))
            self.from_buttons[b] = btn
            from_layout.add_widget(btn)
            
        main_layout.add_widget(from_layout)

        # 3. Экранная клавиатура
        calc_grid = GridLayout(cols=4, spacing=4, size_hint_y=0.35)
        keys = [
            '7', '8', '9', 'C',
            '4', '5', '6', '⌫',
            '1', '2', '3', '0',
            'A', 'B', 'C', 'D',
            'E', 'F', '', ''
        ]
        
        for btn_text in keys:
            if btn_text == '':
                calc_grid.add_widget(Label(size_hint_y=None, height=0))
                continue
            btn = Button(text=btn_text, font_size=16, background_color=(0.25, 0.25, 0.25, 1))
            btn.bind(on_press=self.on_calc_btn_press)
            calc_grid.add_widget(btn)
            
        main_layout.add_widget(calc_grid)
        
        # 4. Перевод В систему
        btn_layout = BoxLayout(orientation='horizontal', spacing=8, size_hint_y=0.08)
        
        btn_bin = Button(text='В 2-ичную', background_color=(0.2, 0.6, 1, 1), font_size=14)
        btn_bin.bind(on_press=lambda x: self.calculate(2))
        
        btn_oct = Button(text='В 8-ичную', background_color=(0.2, 0.8, 0.2, 1), font_size=14)
        btn_oct.bind(on_press=lambda x: self.calculate(8))
        
        btn_dec = Button(text='В 10-ичную', background_color=(0.9, 0.5, 0.1, 1), font_size=14)
        btn_dec.bind(on_press=lambda x: self.calculate(10))
        
        btn_hex = Button(text='В 16-ичную', background_color=(0.8, 0.2, 0.8, 1), font_size=14)
        btn_hex.bind(on_press=lambda x: self.calculate(16))
        
        btn_layout.add_widget(btn_bin)
        btn_layout.add_widget(btn_oct)
        btn_layout.add_widget(btn_dec)
        btn_layout.add_widget(btn_hex)
        main_layout.add_widget(btn_layout)
        
        # 5. Результат и решение
        self.lbl_result = Label(text='Ответ: ', font_size=18, size_hint_y=0.06)
        main_layout.add_widget(self.lbl_result)
        
        scroll = ScrollView(size_hint_y=0.28)
        self.lbl_steps = Label(
            text='Жми цветную кнопку снизу для расчёта', 
            font_size=14, 
            size_hint_y=None, 
            halign='left', 
            valign='top'
        )
        self.lbl_steps.bind(size=lambda inst, val: setattr(inst, 'text_size', (inst.width, None)))
        self.lbl_steps.bind(texture_size=self.lbl_steps.setter('size'))
        
        scroll.add_widget(self.lbl_steps)
        main_layout.add_widget(scroll)
        
        return main_layout

    def set_from_base(self, base):
        self.from_base = base
        for b, btn in self.from_buttons.items():
            btn.background_color = (0.2, 0.6, 1, 1) if b == base else (0.3, 0.3, 0.3, 1)

    def on_calc_btn_press(self, instance):
        val = instance.text
        if val == 'C':
            self.input_num.text = ''
        elif val == '⌫':
            self.input_num.text = self.input_num.text[:-1]
        else:
            self.input_num.text += val

    def calculate(self, to_base):
        raw_text = self.input_num.text.strip().upper()
        if not raw_text:
            self.lbl_result.text = "Ошибка: введите число"
            return
            
        try:
            num = int(raw_text, self.from_base)
        except ValueError:
            self.lbl_result.text = f"Ошибка: неверное число для {self.from_base}-ичной СС"
            return

        hex_digits = "0123456789ABCDEF"
        
        if num == 0:
            self.lbl_result.text = "Ответ: 0"
            self.lbl_steps.text = "0"
            return

        # Вариант А: Перевод ИЗ любой системы В 10-ичную (формула по степеням)
        if to_base == 10 and self.from_base != 10:
            n = len(raw_text)
            steps_text = f"Перевод {raw_text} (из {self.from_base}-ичной в 10-ичную):\n\n"
            steps_text += "Раскладываем по степеням основателя:\n"
            
            powers_terms = []
            values_terms = []
            
            for i, char in enumerate(raw_text):
                power = n - 1 - i
                digit_val = int(char, 16)
                powers_terms.append(f"{char}×{self.from_base}^{power}")
                values_terms.append(str(digit_val * (self.from_base ** power)))
                
            steps_text += " + ".join(powers_terms) + "\n\n"
            steps_text += "= " + " + ".join(values_terms) + f" = [b]{num}[/b]"
            
            self.lbl_result.text = f"Ответ: {num} (10)"
            self.lbl_steps.markup = True
            self.lbl_steps.text = steps_text
            return

        # Вариант Б: Перевод В 2, 8 или 16-ичную (деление на основание)
        temp_num = num
        remainders = []
        steps_text = f"Перевод {raw_text} (из {self.from_base}-ичной) в {to_base}-ичную:\n\n"
        
        if self.from_base != 10:
            steps_text += f"1) В 10-ичной это число = {num}\n2) Деление на {to_base}:\n"
        else:
            steps_text += f"Деление {num} на {to_base}:\n"
            
        while temp_num > 0:
            quotient = temp_num // to_base
            rem = temp_num % to_base
            rem_char = hex_digits[rem]
            remainders.append(rem_char)
            steps_text += f"{temp_num} ÷ {to_base} = {quotient}, остаток: [b]{rem_char}[/b]\n"
            temp_num = quotient
            
        result_str = "".join(remainders[::-1]) if remainders else "0"
        
        self.lbl_result.text = f"Ответ: {result_str} ({to_base})"
        steps_text += f"\nСобираем остатки снизу вверх: {result_str}"
        
        self.lbl_steps.markup = True 
        self.lbl_steps.text = steps_text

if __name__ == '__main__':
    BinaryCalc().run()