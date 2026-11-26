"""Ночная смена в Артондо — небольшая сюжетная игра Baba Alla Universe.

Запуск:
    python "games/Ночная смена в Артондо.py"
Игра не требует сторонних библиотек.
"""
from __future__ import annotations

import random
import textwrap

WIDTH = 68


def line(char: str = "─") -> None:
    print(char * WIDTH)


def say(text: str = "") -> None:
    for paragraph in text.split("\n"):
        print(textwrap.fill(paragraph, WIDTH) if paragraph else "")


def choose(prompt: str, options: list[str]) -> int:
    while True:
        print(f"\n{prompt}")
        for number, option in enumerate(options, 1):
            print(f"  {number}. {option}")
        answer = input("> ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return int(answer) - 1
        print("Нужно выбрать номер из списка.")


class NightShift:
    def __init__(self) -> None:
        self.day = 1
        self.energy = 7
        self.cash = 35
        self.reputation = 0
        self.clues: set[str] = set()
        self.inventory = {"Батарейки": 1, "Изолента": 1}
        self.radio_fixed = False
        self.met_alla = False
        self.running = True

    def status(self) -> None:
        line()
        print(
            f"СМЕНА {self.day}/4  |  Энергия: {self.energy}/10  |  "
            f"Деньги: {self.cash} ₽  |  Репутация: {self.reputation}"
        )
        print("Вещи: " + (", ".join(f"{k} ×{v}" for k, v in self.inventory.items() if v) or "пусто"))
        print("Улики: " + (", ".join(sorted(self.clues)) or "пока нет"))
        line()

    def spend(self, amount: int) -> bool:
        if self.energy < amount:
            say("Ты слишком устал. Сначала придётся передохнуть.")
            return False
        self.energy -= amount
        return True

    def add_item(self, name: str) -> None:
        self.inventory[name] = self.inventory.get(name, 0) + 1
        say(f"Получено: {name}.")

    def use_item(self, name: str) -> bool:
        if self.inventory.get(name, 0) <= 0:
            say(f"У тебя нет предмета «{name}».")
            return False
        self.inventory[name] -= 1
        return True

    def intro(self) -> None:
        line("═")
        say("БАБА АЛЛА: НОЧНАЯ СМЕНА В АРТОНДО")
        line("═")
        say(
            "Артондо. 23:40. Ты заступаешь на ночную смену в маленький "
            "магазинчик у старой автобусной остановки. Хозяин оставил ключи, "
            "кассу и записку: «Если радио заговорит само — не спорь. И чайник "
            "после полуночи не включай»."
        )
        say(
            "До рассвета четыре смены. Нужно разобраться, почему каждую ночь "
            "на пустой остановке кто-то оставляет загадочные послания."
        )
        input("\nНажми Enter, чтобы начать...")

    def shop(self) -> None:
        say("За прилавком лежит коробка с мелочами. Продавец зевает.")
        items = [("Батарейки", 8), ("Изолента", 6), ("Булочка", 5), ("Чай", 4)]
        options = [f"{name} — {price} ₽" for name, price in items] + ["Ничего не покупать"]
        index = choose(f"В кошельке {self.cash} ₽. Что взять?", options)
        if index == len(items):
            return
        name, price = items[index]
        if self.cash < price:
            say("Не хватает денег.")
            return
        self.cash -= price
        self.add_item(name)

    def investigate_stop(self) -> None:
        if not self.spend(2):
            return
        say(
            "На остановке мигает фонарь. Под лавкой лежит мокрый клочок бумаги, "
            "а на расписании кто-то обвёл маршрут № _zero."
        )
        action = choose("Что исследовать?", [
            "Осмотреть записку",
            "Проверить расписание",
            "Заглянуть за остановку",
        ])
        if action == 0:
            self.clues.add("Записка с символом")
            say("На бумаге написано: «Когда часы покажут 03:17, слушай три коротких сигнала».")
        elif action == 1:
            self.clues.add("Маршрут № 0")
            say("Такого маршрута нет. Но кто-то регулярно вписывает его карандашом.")
        else:
            if random.random() < 0.65:
                self.add_item("Старая монета")
                self.clues.add("Монета с буквой А")
                say("В пыли блестит монета с необычной буквой «А».")
            else:
                say("Только мокрые листья и чей-то забытый зонтик.")

    def repair_radio(self) -> None:
        if self.radio_fixed:
            say("Радио уже работает. Из динамика тихо играет старая мелодия.")
            return
        if not self.spend(2):
            return
        if not self.use_item("Батарейки"):
            say("Без батареек радио не оживить.")
            return
        if not self.use_item("Изолента"):
            self.add_item("Батарейки")
            say("Изоленты нет. Ты возвращаешь батарейки в карман.")
            return
        self.radio_fixed = True
        self.clues.add("Три коротких сигнала")
        say(
            "Ты меняешь батарейки, закрепляешь провод изолентой. Радио шипит, "
            "затем выдаёт три коротких сигнала. После паузы голос произносит: "
            "«Артондо помнит тех, кто не проходит мимо»."
        )
        self.reputation += 1

    def meet_alla(self) -> None:
        if self.met_alla:
            say("Баба Алла уже дала тебе своё поручение. Она кивает из-за угла.")
            return
        if not self.spend(1):
            return
        self.met_alla = True
        say(
            "Дверь магазина открывается. На пороге стоит Баба Алла с термосом. "
            "Она смотрит на радио и говорит: «Ну наконец-то. Я думала, ты его "
            "до пенсии чинить будешь»."
        )
        answer = choose("Что ответить?", [
            "Спросить про маршрут № 0",
            "Предложить ей чай",
            "Показать найденную монету",
        ])
        if answer == 0:
            if "Маршрут № 0" in self.clues:
                self.clues.add("История маршрута")
                say("Алла рассказывает: маршрут № 0 возил людей к старому вокзалу, которого уже нет.")
                self.reputation += 2
            else:
                say("«Сначала найди расписание, потом задавай вопросы», — отвечает она.")
        elif answer == 1:
            if self.use_item("Чай"):
                say("Алла довольно кивает и оставляет тебе 10 ₽ на кассе.")
                self.cash += 10
                self.reputation += 1
            else:
                say("«Чай без чая — это просто горячая надежда», — вздыхает Алла.")
        else:
            if self.use_item("Старая монета"):
                self.clues.add("Знак старого вокзала")
                say("Алла узнаёт знак на монете. «Вот теперь разговор серьёзный».")
                self.reputation += 2
            else:
                say("«Будут улики — приходи», — говорит Алла.")

    def random_event(self) -> None:
        event = random.choice([
            ("Пёс у двери", "К магазину прибился пёс. Ты делишься булочкой, и он приносит тебе потерянные 5 ₽.", "Булочка"),
            ("Сбой кассы", "Касса зависла. Ты терпеливо перезапускаешь её и находишь лишние 3 ₽ сдачи.", None),
            ("Тихий час", "Ничего не происходит. Иногда это лучший подарок ночной смены.", None),
        ])
        say(event[1])
        if event[0] == "Пёс у двери" and self.use_item("Булочка"):
            self.cash += 5
            self.reputation += 1
        elif event[0] == "Сбой кассы":
            self.cash += 3

    def end_shift(self) -> None:
        self.energy = min(10, self.energy + 3)
        self.day += 1
        say("\nСмена закончилась. Ты закрываешь магазин и немного отдыхаешь.")
        if self.day <= 4:
            input("Нажми Enter, чтобы перейти к следующей ночи...")

    def ending(self) -> None:
        line("═")
        say("РАССВЕТ НАД АРТОНДО")
        if len(self.clues) >= 4 and self.reputation >= 3 and self.radio_fixed:
            say(
                "На четвёртую ночь радио ловит старую запись: оказывается, маршрут № 0 "
                "был последним рейсом до закрытия вокзала. Баба Алла приходит к рассвету "
                "и вручает тебе выцветший билет. «Теперь история не потеряется». "
                "Ты стал хранителем маленькой тайны Артондо."
            )
            result = "ХРАНИТЕЛЬ ТАЙНЫ"
        elif self.clues:
            say(
                "Ты собрал несколько зацепок. Полная история пока ускользает, "
                "но Артондо уже не кажется обычным городком. Алла обещает продолжить расследование."
            )
            result = "СЛЕДОПЫТ"
        else:
            say(
                "Ночь прошла спокойно. Никаких разгадок — зато магазин цел, "
                "касса сходится, а чайник так и не включали."
            )
            result = "СПОКОЙНАЯ СМЕНА"
        print(f"\nТВОЙ ИТОГ: {result}")
        line("═")

    def run(self) -> None:
        self.intro()
        while self.day <= 4:
            self.status()
            say(f"Ночь {self.day}. До рассвета ещё есть время.")
            action = choose("Куда направишься?", [
                "Исследовать автобусную остановку (2 энергии)",
                "Зайти в магазин за припасами",
                "Починить радио (2 энергии)",
                "Поговорить с Бабой Аллой (1 энергия)",
                "Сделать перерыв и закончить смену",
            ])
            if action == 0:
                self.investigate_stop()
            elif action == 1:
                self.shop()
            elif action == 2:
                self.repair_radio()
            elif action == 3:
                self.meet_alla()
            else:
                self.end_shift()
                continue
            if self.day <= 4 and random.random() < 0.25:
                self.random_event()
            if self.energy == 0:
                say("Сил больше нет. Смена окончена досрочно.")
                self.day = 5
        self.ending()


if __name__ == "__main__":
    try:
        NightShift().run()
    except (KeyboardInterrupt, EOFError):
        print("\nСмена прервана. Баба Алла закрыла магазин за тебя.")
