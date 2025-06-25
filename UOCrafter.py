import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QComboBox, QLineEdit, QPushButton, QListWidget, QLabel,
                             QMessageBox, QTextBrowser, QCompleter, QListWidgetItem)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

class ShoppingListApp(QWidget):
    # Slownik definiujacy zasoby potrzebne do wytworzenia kazdego artykulu
    CRAFTING_RESOURCES = {
        "tworzenie_lukuw": {"sztaby": 4, "deski": 2, "klejnoty": 0},
        "mlotek_kowalski": {"sztaby": 4, "deski": 0, "klejnoty": 0},
        "mlot_kowalski": {"sztaby": 5, "deski": 0, "klejnoty": 0},
        "wytrych": {"sztaby": 1, "deski": 0, "klejnoty": 0}, # Przyklad: wytrych nie wymaga sztab
        "kilof": {"sztaby": 5, "deski": 0, "klejnoty": 0},   # Przyklad: kilof nie wymaga desek
        "sierp": {"sztaby": 4, "deski": 0, "klejnoty": 0},
        "mozdzierz": {"sztaby": 4, "deski": 0, "klejnoty": 0},
        "narzedzie_szklarskie": {"sztaby": 4, "deski": 0, "klejnoty": 0},
        "narzedzia_naprawcze": {"sztaby": 2, "deski": 0, "klejnoty": 0},
        "narzedzia_druciarza": {"sztaby": 4, "deski": 0, "klejnoty": 0},
        "narzedzia_szewskie": {"sztaby": 4, "deski": 0, "klejnoty": 0},
        "pila": {"sztaby": 4, "deski": 0, "klejnoty": 0},
        "dluto": {"sztaby": 2, "deski": 4, "klejnoty": 0},
        "kolczyki": {"sztaby": 1, "deski": 0, "klejnoty": 1},
        "zloty_naszyjnik": {"sztaby": 1, "deski": 0, "klejnoty": 1},
        "szpony": {"sztaby": 4, "deski": 0, "klejnoty": 0},
        "tekagi": {"sztaby": 6, "deski": 0, "klejnoty": 0},
        "ciemne_jingasa": {"sztaby": 12, "deski": 0, "klejnoty": 0},
        "plytowe_jingasa": {"sztaby": 9, "deski": 0, "klejnoty": 0},
        "diadem": {"sztaby": 4, "deski": 0, "klejnoty": 10},
        "swiecznikA": {"sztaby": 4, "deski": 0, "klejnoty": 0},
        "swiecznikB": {"sztaby": 15, "deski": 0, "klejnoty": 0},
        "swieczka": {"sztaby": 2, "deski": 0, "klejnoty": 0},
        "waga": {"sztaby": 5, "deski": 0, "klejnoty": 0},
        "lichtarzykA": {"sztaby": 5, "deski": 0, "klejnoty": 0},
        "lichtarzykB": {"sztaby": 5, "deski": 0, "klejnoty": 0},
        "luneta": {"sztaby": 4, "deski": 0, "klejnoty": 0},
        "bola": {"sztaby": 2, "deski": 0, "klejnoty": 0},
        "czesci_do_zegara": {"sztaby": 1, "deski": 0, "klejnoty": 0},
        "kurek_do_beczki": {"sztaby": 1, "deski": 0, "klejnoty": 0},
        "obrecz": {"sztaby": 5, "deski": 0, "klejnoty": 0},
        "narzedzia_stolarskie": {"sztaby": 0, "deski": 4, "klejnoty": 0},
        "globus": {"sztaby": 0, "deski": 5, "klejnoty": 0},
        "paleta": {"sztaby": 0, "deski": 4, "klejnoty": 0},
        "pioro": {"sztaby": 0, "deski": 4, "klejnoty": 0},
        "pioro_kartografa": {"sztaby": 0, "deski": 4, "klejnoty": 0}
    }

    # Listy dla typow sztab i desek (bez "Brak materialu" jako elementu do wyboru, gdy jest wymagany)
    METAL_TYPES = ["zelazo", "zloto", "srebro", "veryt", "blackrock",
                   "agapit", "valoryt", "mytheril", "azuryt", "bloodrock", "royal", "grafit"]
    WOOD_TYPES = ["zwykle", "dab", "orzech", "cedr", "cis", "cyprys"]
    
    # Stale dla opcji "Brak materialu"
    NO_MATERIAL_OPTION = "Brak materialu"
    DATA_FILE = "crafter_list_data.json" # Nazwa pliku do zapisu/odczytu danych

    def __init__(self):
        super().__init__()
        self.is_dark_theme = True # Flaga do sledzenia aktualnego motywu
        self.unsaved_changes = False # Nowa flaga do sledzenia niezapisanych zmian
        self.initUI()
        self.set_dark_mode() # Ustawienie poczatkowego motywu na ciemny
        self.load_data_on_startup() # Proba wczytania danych przy starcie aplikacji

    def initUI(self):
        # Ustawienia okna glownego
        self.setWindowTitle('UOCrafter') # Zmieniona nazwa aplikacji
        self.setGeometry(100, 100, 580, 680)

        # Glowny uklad pionowy dla calego okna
        main_layout = QVBoxLayout()

        # Sekcja dodawania artykulow (uklad poziomy dla elementow wejsciowych)
        add_item_layout = QHBoxLayout()

        # Etykieta dla QComboBox artykulow
        add_item_layout.addWidget(QLabel("Wybierz artykul:"))

        # QComboBox - rozwijana lista artykulow (z autouzupełnianiem)
        self.item_combo = QComboBox(self)
        self.item_combo.setEditable(True) # Umozliwia wpisywanie tekstu
        self.item_combo.addItems(list(self.CRAFTING_RESOURCES.keys()))
        # Ustawienie QCompleter dla listy artykulow
        self.completer_item = QCompleter(list(self.CRAFTING_RESOURCES.keys()), self.item_combo)
        self.completer_item.setCaseSensitivity(Qt.CaseInsensitive) # Nieczula na wielkosc liter
        self.completer_item.setFilterMode(Qt.MatchContains) # Proponuje pozycje zawierajace wpisany tekst
        self.completer_item.setCompletionMode(QCompleter.PopupCompletion) # Wyswietla w popupie
        self.item_combo.setCompleter(self.completer_item)
        self.item_combo.currentIndexChanged.connect(self.update_material_combos_state)
        add_item_layout.addWidget(self.item_combo)

        # Etykieta i QComboBox dla rodzaju sztab (z autouzupełnianiem)
        add_item_layout.addWidget(QLabel("Rodzaj sztab:"))
        self.metal_type_combo = QComboBox(self)
        self.metal_type_combo.setEditable(True) # Umozliwia wpisywanie tekstu
        # Poczatkowo dodajemy tylko METAL_TYPES. NO_MATERIAL_OPTION bedzie dodane dynamicznie jesli potrzeba.
        self.metal_type_combo.addItems(self.METAL_TYPES)
        # Ustawienie QCompleter dla listy sztab
        self.completer_metal = QCompleter(self.METAL_TYPES, self.metal_type_combo)
        self.completer_metal.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer_metal.setFilterMode(Qt.MatchContains)
        self.completer_metal.setCompletionMode(QCompleter.PopupCompletion)
        self.metal_type_combo.setCompleter(self.completer_metal)
        
        # Ustaw domyslna wartosc na "zelazo"
        if "zelazo" in self.METAL_TYPES:
            self.metal_type_combo.setCurrentIndex(self.metal_type_combo.findText("zelazo"))
        else: # Fallback jesli "zelazo" nie istnieje
            self.metal_type_combo.setCurrentIndex(0) # Wybierz pierwszy element

        add_item_layout.addWidget(self.metal_type_combo)

        # Etykieta i QComboBox dla rodzaju desek (z autouzupełnianiem)
        add_item_layout.addWidget(QLabel("Rodzaj desek:"))
        self.wood_type_combo = QComboBox(self)
        self.wood_type_combo.setEditable(True) # Umozliwia wpisywanie tekstu
        # Poczatkowo dodajemy tylko WOOD_TYPES. NO_MATERIAL_OPTION bedzie dodane dynamicznie jesli potrzeba.
        self.wood_type_combo.addItems(self.WOOD_TYPES)
        # Ustawienie QCompleter dla listy desek
        self.completer_wood = QCompleter(self.WOOD_TYPES, self.wood_type_combo)
        self.completer_wood.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer_wood.setFilterMode(Qt.MatchContains)
        self.completer_wood.setCompletionMode(QCompleter.PopupCompletion)
        self.wood_type_combo.setCompleter(self.completer_wood)
        
        # Ustaw domyslna wartosc na "zwykle"
        if "zwykle" in self.WOOD_TYPES:
            self.wood_type_combo.setCurrentIndex(self.wood_type_combo.findText("zwykle"))
        else: # Fallback jesli "zwykle" nie istnieje
            self.wood_type_combo.setCurrentIndex(0) # Wybierz pierwszy element

        add_item_layout.addWidget(self.wood_type_combo)

        # Etykieta dla QLineEdit ilosci
        add_item_layout.addWidget(QLabel("Ilosc:"))

        # QLineEdit - pole tekstowe na ilosc
        self.quantity_input = QLineEdit(self)
        self.quantity_input.setPlaceholderText("Wprowadz ilosc")
        self.quantity_input.setFixedWidth(80)
        add_item_layout.addWidget(self.quantity_input)

        # QPushButton - przycisk "Dodaj do listy"
        add_button = QPushButton("Dodaj do listy", self)
        add_button.clicked.connect(self.add_item_to_list)
        add_item_layout.addWidget(add_button)

        main_layout.addLayout(add_item_layout)

        # QListWidget - wyswietla aktualna liste zakupow
        main_layout.addWidget(QLabel("Twoja lista itemow:"))
        self.shopping_list_widget = QListWidget(self)
        main_layout.addWidget(self.shopping_list_widget)

        # Uklad dla przyciskow usuwania i eksportu
        action_buttons_layout = QHBoxLayout()

        # QPushButton - przycisk "Usun zaznaczone"
        remove_selected_button = QPushButton("Usun zaznaczone", self)
        remove_selected_button.clicked.connect(self.remove_selected_item)
        action_buttons_layout.addWidget(remove_selected_button)

        # QPushButton - przycisk "Usun wszystko"
        remove_all_button = QPushButton("Usun wszystko", self)
        remove_all_button.clicked.connect(self.remove_all_items)
        action_buttons_layout.addWidget(remove_all_button)

        # QPushButton - przycisk "Eksportuj do pliku" (z czerwonym akcentem)
        self.export_button = QPushButton("Eksportuj do pliku", self)
        self.export_button.clicked.connect(self.export_list_to_file)
        self.export_button.setStyleSheet(
            "QPushButton { background-color: #DC3545; color: white; border-radius: 5px; padding: 5px; }"
            "QPushButton:hover { background-color: #C82333; }"
        )
        action_buttons_layout.addWidget(self.export_button)

        main_layout.addLayout(action_buttons_layout)

        # Etykiety do wyswietlania sumy zasobow (globalne)
        totals_label = QLabel("Wymagane zasoby (suma):")
        main_layout.addWidget(totals_label)

        self.total_sztaby_label = QLabel("Sztaby: 0")
        self.total_deski_label = QLabel("Deski: 0")
        self.total_klejnoty_label = QLabel("Klejnoty: 0")

        # Uklad poziomy dla sumy zasobow globalnych
        totals_layout = QHBoxLayout()
        totals_layout.addWidget(self.total_sztaby_label)
        totals_layout.addWidget(self.total_deski_label)
        totals_layout.addWidget(self.total_klejnoty_label)
        main_layout.addLayout(totals_layout)

        # Etykieta i QTextBrowser do wyswietlania sumy zasobow wedlug typu materialu
        material_type_totals_label = QLabel("Wymagane zasoby (wg typu materialu):")
        main_layout.addWidget(material_type_totals_label)
        self.material_totals_display = QTextBrowser(self)
        self.material_totals_display.setMinimumHeight(120)
        main_layout.addWidget(self.material_totals_display)

        # Nowy uklad dla przyciskow akcji dolnych i napisu atrybucji
        bottom_controls_layout = QHBoxLayout()

        # Przycisk "Zapisz zmiany"
        self.save_button = QPushButton("Zapisz zmiany", self)
        self.save_button.clicked.connect(self.save_data)
        bottom_controls_layout.addWidget(self.save_button)

        # Przycisk "Wczytaj zmiany"
        self.load_button = QPushButton("Wczytaj zmiany", self)
        self.load_button.clicked.connect(self.load_data)
        bottom_controls_layout.addWidget(self.load_button)

        # Przycisk do przelaczania motywu (mniejszy, po lewej, obok przyciskow zapisu/odczytu)
        self.theme_toggle_button = QPushButton("Przelacz Motyw", self)
        self.theme_toggle_button.clicked.connect(self.toggle_theme)
        self.theme_toggle_button.setFixedSize(120, 30) # Ustawienie stalego, mniejszego rozmiaru
        bottom_controls_layout.addWidget(self.theme_toggle_button)
        
        # Rozpychacz, aby napis atrybucji byl po prawej
        bottom_controls_layout.addStretch(1) 

        # Napis atrybucji (po prawej)
        attribution_label = QLabel("Created by RichRichie with Gemini 2.5 Flash")
        attribution_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        bottom_controls_layout.addWidget(attribution_label)
        
        main_layout.addLayout(bottom_controls_layout) # Dodaj uklad do glownego ukladu

        self.setLayout(main_layout)

        # Wywolaj aktualizacje stanow comboboxow i sum przy starcie
        self.update_material_combos_state()
        self.calculate_totals() 

    def closeEvent(self, event):
        """
        Obsluguje zdarzenie zamkniecia okna. Pyta uzytkownika o zapisanie zmian,
        jesli istnieja niezapisane zmiany.
        """
        if self.unsaved_changes:
            reply = QMessageBox.question(self, 'Niezapisane zmiany',
                                         "Masz niezapisane zmiany. Czy chcesz je zapisac przed zamknieciem?",
                                         QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                                         QMessageBox.Save)
            if reply == QMessageBox.Save:
                self.save_data() # Zapisz dane
                event.accept() # Kontynuuj zamykanie
            elif reply == QMessageBox.Discard:
                event.accept() # Zamknij bez zapisu
            else:
                event.ignore() # Anuluj zamykanie
        else:
            event.accept() # Zamknij bez pytania, jesli brak zmian


    def set_dark_mode(self):
        """Ustawia motyw aplikacji na ciemny."""
        palette = QApplication.instance().palette() # Pobierz biezaca palete
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        QApplication.instance().setPalette(palette)
        self.is_dark_theme = True

    def set_light_mode(self):
        """Ustawia motyw aplikacji na jasny."""
        palette = QApplication.instance().palette() # Pobierz biezaca palete
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
        palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.Button, QColor(200, 200, 200))
        palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(0, 0, 238))
        palette.setColor(QPalette.Highlight, QColor(140, 180, 255))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        QApplication.instance().setPalette(palette)
        self.is_dark_theme = False

    def toggle_theme(self):
        """Przelacza miedzy motywem ciemnym a jasnym."""
        if self.is_dark_theme:
            self.set_light_mode()
        else:
            self.set_dark_mode()

    def update_material_combos_state(self):
        """
        Aktualizuje stan (enabled/disabled) i wybrane opcje
        dla rozwijanych list typow materialow na podstawie wybranego artykulu.
        """
        selected_item = self.item_combo.currentText()
        resources = self.CRAFTING_RESOURCES.get(selected_item, {"sztaby": 0, "deski": 0, "klejnoty": 0})

        # --- Obsluga dla sztab ---
        if resources["sztaby"] == 0:
            self.metal_type_combo.clear() # Wyczyść liste
            self.metal_type_combo.addItem(self.NO_MATERIAL_OPTION) # Dodaj tylko "Brak materialu"
            self.metal_type_combo.setCurrentText(self.NO_MATERIAL_OPTION)
            self.metal_type_combo.setEnabled(False)
            self.metal_type_combo.setEditable(False) # Nie da sie wpisywac
            #self.completer_metal.setModel(self.metal_type_combo.model()) # Zaktualizuj model completera
            # Ustaw model completera na model, ktory zawiera tylko "Brak materialu"
            self.completer_metal.setModel(self.metal_type_combo.model()) 
        else:
            self.metal_type_combo.setEnabled(True)
            self.metal_type_combo.setEditable(True)
            
            previous_selection = self.metal_type_combo.currentText() # Zapisz poprzedni wybor

            self.metal_type_combo.clear() # Wyczyść liste
            self.metal_type_combo.addItems(self.METAL_TYPES) # Dodaj tylko typy materialow
            #self.completer_metal.setModel(self.metal_type_combo.model()) # Zaktualizuj model completera
            # Ustaw model completera na model z pelna lista materialow
            self.completer_metal.setModel(self.metal_type_combo.model()) 

            # Sproboj przywrocic poprzedni wybor lub ustaw domyslny
            if previous_selection in self.METAL_TYPES:
                self.metal_type_combo.setCurrentText(previous_selection)
            elif "zelazo" in self.METAL_TYPES:
                self.metal_type_combo.setCurrentText("zelazo")
            elif self.METAL_TYPES: # Fallback do pierwszego elementu jesli "zelazo" nie ma
                self.metal_type_combo.setCurrentText(self.METAL_TYPES[0])
            else: # Gdy METAL_TYPES jest puste (mala szansa)
                self.metal_type_combo.setCurrentText(self.NO_MATERIAL_OPTION)


        # --- Obsluga dla desek ---
        if resources["deski"] == 0:
            self.wood_type_combo.clear()
            self.wood_type_combo.addItem(self.NO_MATERIAL_OPTION)
            self.wood_type_combo.setCurrentText(self.NO_MATERIAL_OPTION)
            self.wood_type_combo.setEnabled(False)
            self.wood_type_combo.setEditable(False)
            self.completer_wood.setModel(self.wood_type_combo.model())
        else:
            self.wood_type_combo.setEnabled(True)
            self.wood_type_combo.setEditable(True)

            previous_selection = self.wood_type_combo.currentText()

            self.wood_type_combo.clear()
            self.wood_type_combo.addItems(self.WOOD_TYPES)
            self.completer_wood.setModel(self.wood_type_combo.model())

            if previous_selection in self.WOOD_TYPES:
                self.wood_type_combo.setCurrentText(previous_selection)
            elif "zwykle" in self.WOOD_TYPES:
                self.wood_type_combo.setCurrentText("zwykle")
            elif self.WOOD_TYPES:
                self.wood_type_combo.setCurrentText(self.WOOD_TYPES[0])
            else:
                self.wood_type_combo.setCurrentText(self.NO_MATERIAL_OPTION)


    def add_item_to_list(self):
        """
        Metoda dodaje wybrany artykul z podana iloscia, typem sztab i desek do listy zakupow.
        Wykonuje walidacje wprowadzonej ilosci.
        Przechowuje dane artykulu i obliczone zasoby w obiekcie QListWidgetItem.
        """
        selected_item = self.item_combo.currentText()
        selected_metal_type = self.metal_type_combo.currentText()
        selected_wood_type = self.wood_type_combo.currentText()
        quantity_text = self.quantity_input.text()

        # Walidacja czy wybrany artykul istnieje
        if selected_item not in self.CRAFTING_RESOURCES:
            QMessageBox.warning(self, "Blad Wprowadzania", "Wybrany artykul nie istnieje na liscie do craftingu!")
            return

        if not quantity_text.strip():
            QMessageBox.warning(self, "Blad Wprowadzania", "Prosze podac ilosc!")
            return

        try:
            quantity = int(quantity_text)
            if quantity <= 0:
                QMessageBox.warning(self, "Blad Wprowadzania", "Ilosc musi byc dodatnia!")
                return
        except ValueError:
            QMessageBox.warning(self, "Blad Wprowadzania", "Wprowadz poprawna liczbe!")
            return

        item_resources_base = self.CRAFTING_RESOURCES.get(selected_item, {"sztaby": 0, "deski": 0, "klejnoty": 0})
        
        # Oblicz calkowite zasoby dla tej pozycji (ilosc * zasoby_na_sztuke)
        total_item_resources = {
            "sztaby": item_resources_base["sztaby"] * quantity,
            "deski": item_resources_base["deski"] * quantity,
            "klejnoty": item_resources_base["klejnoty"] * quantity
        }

        # Okreslenie przewazajacego materialu dla wyswietlenia i eksportu
        # Uwzglednij, ze wybrane typy materialow moga byc "Brak materialu"
        predominant_material_for_display = self.NO_MATERIAL_OPTION

        if item_resources_base["sztaby"] > item_resources_base["deski"] and selected_metal_type != self.NO_MATERIAL_OPTION:
            predominant_material_for_display = selected_metal_type
        elif item_resources_base["deski"] > item_resources_base["sztaby"] and selected_wood_type != self.NO_MATERIAL_OPTION:
            predominant_material_for_display = selected_wood_type
        elif item_resources_base["sztaby"] == item_resources_base["deski"]:
            # Jesli ilosci zasobow sa rowne (i nie sa zerowe), wybierz preferowany typ
            if selected_metal_type != self.NO_MATERIAL_OPTION:
                predominant_material_for_display = selected_metal_type
            elif selected_wood_type != self.NO_MATERIAL_OPTION:
                predominant_material_for_display = selected_wood_type
            # Jesli oba sa "Brak materialu", predominant_material_for_display pozostanie NO_MATERIAL_OPTION

        # Utworz sformatowany ciag znakow do dodania na liste
        display_text = f"{selected_item} ({predominant_material_for_display}) - Ilosc: {quantity}"
        # Dodaj informacje o konkretnych typach sztab i desek
        display_text += f" [Sztaby: {selected_metal_type}]"
        display_text += f" [Deski: {selected_wood_type}]"

        list_item = self.shopping_list_widget.addItem(display_text)
        # Przechowaj wszystkie potrzebne dane w QListWidgetItem
        self.shopping_list_widget.item(self.shopping_list_widget.count() - 1).setData(
            Qt.UserRole, {
                'article': selected_item,
                'metal_type': selected_metal_type,
                'wood_type': selected_wood_type,
                'quantity': quantity,
                'resources': total_item_resources, # Zasoby ogolne dla tej pozycji
                'predominant_material_display': predominant_material_for_display # Material przewazajacy do eksportu
            }
        )
        self.unsaved_changes = True # Zmiana nastapila, ustaw flage

        self.quantity_input.clear()
        self.calculate_totals() # Zaktualizuj sumy zasobow

    def remove_selected_item(self):
        """
        Metoda usuwa wszystkie zaznaczone elementy z listy zakupow.
        """
        list_items = self.shopping_list_widget.selectedItems()
        if not list_items: return

        for item in list_items:
            self.shopping_list_widget.takeItem(self.shopping_list_widget.row(item))
        
        if list_items: # Jesli cokolwiek usunieto, oznacz zmiany
            self.unsaved_changes = True
        self.calculate_totals() # Zaktualizuj sumy zasobow po usunieciu

    def remove_all_items(self):
        """
        Metoda usuwa wszystkie elementy z listy zakupow.
        """
        if self.shopping_list_widget.count() > 0: # Tylko jesli cos jest do usuniecia
            self.shopping_list_widget.clear()
            QMessageBox.information(self, "Lista Wyczysc", "Wszystkie elementy zostaly usuniete z listy.")
            self.unsaved_changes = True # Zmiana nastapila, ustaw flage
        self.calculate_totals() # Zaktualizuj sumy zasobow po usunieciu wszystkiego

    def save_data(self):
        """
        Zapisuje aktualny stan listy zakupow do pliku JSON.
        """
        data_to_save = []
        for i in range(self.shopping_list_widget.count()):
            item = self.shopping_list_widget.item(i)
            item_data = item.data(Qt.UserRole)
            if item_data:
                # Zapisz tylko te dane, ktore sa potrzebne do odtworzenia stanu
                data_to_save.append({
                    'article': item_data.get('article'),
                    'metal_type': item_data.get('metal_type'),
                    'wood_type': item_data.get('wood_type'),
                    'quantity': item_data.get('quantity')
                })
        
        try:
            with open(self.DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4)
            QMessageBox.information(self, "Zapisano", f"Dane zostaly zapisane do pliku: {self.DATA_FILE}")
            self.unsaved_changes = False # Zapisano zmiany, resetuj flage
        except Exception as e:
            QMessageBox.critical(self, "Blad Zapisu", f"Wystapil blad podczas zapisu danych: {e}")

    def load_data(self, show_message=True):
        """
        Wczytuje stan listy zakupow z pliku JSON.
        :param show_message: Czy wyswietlic QMessageBox po wczytaniu danych.
        """
        if not os.path.exists(self.DATA_FILE):
            if show_message:
                QMessageBox.information(self, "Wczytywanie", "Plik z danymi nie istnieje. Rozpoczeto pusta liste.")
            return

        try:
            with open(self.DATA_FILE, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
            
            self.shopping_list_widget.clear() # Wyczyść biezaca liste przed wczytaniem
            for item_data_raw in loaded_data:
                article = item_data_raw.get('article')
                metal_type = item_data_raw.get('metal_type')
                wood_type = item_data_raw.get('wood_type')
                quantity = item_data_raw.get('quantity')

                if not all([article, isinstance(quantity, int)]):
                    # Pomijanie blednych wpisow
                    print(f"Ostrzezenie: Pominiento niekompletny wpis: {item_data_raw}")
                    continue

                # Recalculate resources and predominant material for display/storage
                item_resources_base = self.CRAFTING_RESOURCES.get(article, {"sztaby": 0, "deski": 0, "klejnoty": 0})
                total_item_resources = {
                    "sztaby": item_resources_base["sztaby"] * quantity,
                    "deski": item_resources_base["deski"] * quantity,
                    "klejnoty": item_resources_base["klejnoty"] * quantity
                }

                predominant_material_for_display = self.NO_MATERIAL_OPTION
                if item_resources_base["sztaby"] > item_resources_base["deski"] and metal_type != self.NO_MATERIAL_OPTION:
                    predominant_material_for_display = metal_type
                elif item_resources_base["deski"] > item_resources_base["sztaby"] and wood_type != self.NO_MATERIAL_OPTION:
                    predominant_material_for_display = wood_type
                elif item_resources_base["sztaby"] == item_resources_base["deski"]:
                    if metal_type != self.NO_MATERIAL_OPTION:
                        predominant_material_for_display = metal_type
                    elif wood_type != self.NO_MATERIAL_OPTION:
                        predominant_material_for_display = wood_type
                
                # Odtworz tekst wyswietlany na liscie
                display_text = f"{article} ({predominant_material_for_display}) - Ilosc: {quantity}"
                display_text += f" [Sztaby: {metal_type}]"
                display_text += f" [Deski: {wood_type}]"

                # Zmiana: Jawne utworzenie QListWidgetItem przed ustawieniem danych i dodaniem do listy
                new_list_item = QListWidgetItem(display_text)
                new_list_item.setData(Qt.UserRole, {
                    'article': article,
                    'metal_type': metal_type,
                    'wood_type': wood_type,
                    'quantity': quantity,
                    'resources': total_item_resources,
                    'predominant_material_display': predominant_material_for_display
                })
                self.shopping_list_widget.addItem(new_list_item) # Dodajemy przygotowany element

            self.calculate_totals() # Zaktualizuj sumy po wczytaniu
            self.update_material_combos_state() # Zaktualizuj stan comboboxow po wczytaniu
            if show_message:
                QMessageBox.information(self, "Wczytano", "Dane zostaly wczytane pomyslnie.")
            self.unsaved_changes = False # Wczytano zmiany, resetuj flage
        except json.JSONDecodeError as e:
            if show_message:
                QMessageBox.critical(self, "Blad Wczytywania", f"Blad dekodowania pliku JSON: {e}")
            self.unsaved_changes = True # Jesli blad, traktuj jako potencjalnie niepoprawny stan
        except Exception as e:
            if show_message:
                QMessageBox.critical(self, "Blad Wczytywania", f"Wystapil blad podczas wczytywania danych: {e}")
            self.unsaved_changes = True # Jesli blad, traktuj jako potencjalnie niepoprawny stan

    def load_data_on_startup(self):
        """
        Wczytuje dane przy starcie aplikacji, ale bez wyswietlania komunikatu
        jesli plik nie istnieje lub wystapia bledy.
        """
        self.load_data(show_message=False)


    def export_list_to_file(self):
        """
        Metoda eksportuje cala liste zakupow do pliku craft_ItemList.txt.
        Format pliku: artykul;przewazajacy_material;ilosc w oddzielnych liniach.
        """
        file_name = "craft_ItemList.txt"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, file_name)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                for i in range(self.shopping_list_widget.count()):
                    item = self.shopping_list_widget.item(i)
                    item_data = item.data(Qt.UserRole)
                    
                    article = item_data.get('article', 'Nieznany artykul')
                    # Uzyj predominant_material_display do eksportu jako "kolor"
                    predominant_material = item_data.get('predominant_material_display', self.NO_MATERIAL_OPTION)
                    quantity = item_data.get('quantity', 0)

                    f.write(f"{article};{predominant_material};{quantity}\n")
            
            QMessageBox.information(self, "Eksport Zakonczony", f"Lista zostala pomyslnie wyeksportowana do pliku:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Blad Eksportu", f"Wystapil blad podczas eksportowania listy: {e}")

    def calculate_totals(self):
        """
        Oblicza sume zasobow dla wszystkich artykulow na liscie (globalnie)
        oraz sumy dla poszczegolnych typow sztab i desek, aktualizujac etykiety i QTextBrowser.
        """
        total_sztaby_global = 0
        total_deski_global = 0
        total_klejnoty_global = 0
        
        # Slowniki do przechowywania sum zasobow dla kazdego typu materialu
        metal_type_totals = {metal: 0 for metal in self.METAL_TYPES}
        wood_type_totals = {wood: 0 for wood in self.WOOD_TYPES}

        for i in range(self.shopping_list_widget.count()):
            item = self.shopping_list_widget.item(i)
            item_data = item.data(Qt.UserRole)
            
            if item_data and 'resources' in item_data:
                resources_for_item = item_data['resources']
                selected_metal_type = item_data.get('metal_type')
                selected_wood_type = item_data.get('wood_type')

                # Sumowanie globalne
                total_sztaby_global += resources_for_item.get('sztaby', 0)
                total_deski_global += resources_for_item.get('deski', 0)
                total_klejnoty_global += resources_for_item.get('klejnoty', 0)

                # Sumowanie wedlug typu materialu (jesli wybrano konkretny typ i nie jest "Brak materialu")
                if selected_metal_type != self.NO_MATERIAL_OPTION and selected_metal_type in metal_type_totals:
                    metal_type_totals[selected_metal_type] += resources_for_item.get('sztaby', 0)
                
                if selected_wood_type != self.NO_MATERIAL_OPTION and selected_wood_type in wood_type_totals:
                    wood_type_totals[selected_wood_type] += resources_for_item.get('deski', 0)
        
        # Zaktualizuj tekst etykiet globalnych
        self.total_sztaby_label.setText(f"Sztaby (suma): {total_sztaby_global}")
        self.total_deski_label.setText(f"Deski (suma): {total_deski_global}")
        self.total_klejnoty_label.setText(f"Klejnoty (suma): {total_klejnoty_global}")

        # Zaktualizuj QTextBrowser dla sum wedlug typu materialu
        material_html = "<h3>Sztaby i deski wg typu materialu:</h3>"
        
        # Sekcja dla sztab
        material_html += "<h4>Sztaby:</h4>"
        has_metal_totals = False
        for metal_type in self.METAL_TYPES: # Iteruj po wszystkich mozliwych typach, zeby pokazac nawet 0
            total_qty = metal_type_totals.get(metal_type, 0)
            if total_qty > 0:
                has_metal_totals = True
                material_html += f"<p><b>{metal_type}:</b> {total_qty}</p>"
        if not has_metal_totals:
            material_html += "<p>Brak wymagan na sztaby.</p>"

        # Sekcja dla desek
        material_html += "<h4>Deski:</h4>"
        has_wood_totals = False
        for wood_type in self.WOOD_TYPES: # Iteruj po wszystkich mozliwych typach, zeby pokazac nawet 0
            total_qty = wood_type_totals.get(wood_type, 0)
            if total_qty > 0:
                has_wood_totals = True
                material_html += f"<p><b>{wood_type}:</b> {total_qty}</p>"
        if not has_wood_totals:
            material_html += "<p>Brak wymagan na deski.</p>"

        self.material_totals_display.setHtml(material_html)


# Punkt wejscia do aplikacji
if __name__ == '__main__':
    # Dodanie argumentu do sys.argv, aby wymusic ciemny motyw na ramce okna Windows
    # Nalezy pamietac, ze to dziala tylko na Windows i wymaga odpowiednich ustawien systemowych
    sys.argv.append('-platformplugin')
    sys.argv.append('windows')
    sys.argv.append('-platform')
    sys.argv.append('windows:darkmode=1')

    app = QApplication(sys.argv)

    # Ustawienie stylu "Fusion" dla lepszej konsystencji motywu wewnatrz aplikacji
    app.setStyle("Fusion") 
    
    # Utworzenie instancji aplikacji i ustawienie poczatkowego motywu
    ex = ShoppingListApp()
    ex.show()
    sys.exit(app.exec_())
