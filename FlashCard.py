import typing
from PyQt5 import QtCore, QtWidgets 
from PyQt5.QtWidgets import QApplication, QMainWindow,QInputDialog,QLineEdit,QMessageBox,QColorDialog,QFileDialog
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QTextCursor, QTextCharFormat,QFont,QTextListFormat,QTextBlockFormat,QTextImageFormat,QPixmap
import sys
import json

from Main_Window import Ui_MainWindow
from Add_basic_window import Ui_AddFlashCard
from select_image_window import Ui_ImgSelectWindow
from image_editing_window import Ui_ImgEditWindow

class FlashCardApp(QMainWindow):
    #constructor of FlashCardApp Class
    def __init__(self):
        super(FlashCardApp, self).__init__()

        #creat object of ui class that we create import from Main_Window file  
        self.ui=Ui_MainWindow() 
        self.ui.setupUi(self)
        self.ui.deck_name_list_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.deck_name_list_widget.customContextMenuRequested.connect(self.ui.showContextMenu)


        self.add_window=QtWidgets.QMainWindow()
        self.add_card_ui =Ui_AddFlashCard()
        self.add_card_ui.setupUi(self.add_window) 

        self.image_edit_window =QtWidgets.QMainWindow()
        self.imgEdit_ui=Ui_ImgEditWindow()
        self.imgEdit_ui.setupUi(self.image_edit_window)


        self.image_select_window =QtWidgets.QMainWindow()
        self.imgSelect_ui=Ui_ImgSelectWindow()
        self.imgSelect_ui.setupUi(self.image_select_window)

        #List Of Deck Name
        self.deck_list=[]

        #Dictionary of Key:deck with value:list of new,learn,due count and cards name of deck
        self.dic={}

        #load all previous decks
        self.Load_Decks()

        self.current_index=self.ui.deck_name_list_widget.currentRow()
        self.ui.new_list_widget.setCurrentRow(self.current_index)
        self.ui.learn_list_widget.setCurrentRow(self.current_index)
        self.ui.due_list_widget.setCurrentRow(self.current_index)

        self.ui.dark_mode_radio_button.clicked.connect(self.Toggle_dark_mode)
        self.ui.create_deck_button.clicked.connect(self.Add_deck) 
        self.ui.actionExit.triggered.connect(self.exit)

        self.ui.add_button.clicked.connect(self.Add_FlashCard)

        self.ui.rename_action.triggered.connect(self.Rename_deck)
        self.ui.remove_action.triggered.connect(self.Remove_deck)
        self.ui.add_deck.triggered.connect(self.Add_deck)
        self.ui.movedown_action.triggered.connect(self.Move_down_deck)
        self.ui.moveup_action.triggered.connect(self.Move_up_deck)

        #create tool boxobject
        self.add_card_ui.bold_button.clicked.connect(self.format_text_bold)
        self.add_card_ui.italic_button.clicked.connect(self.format_text_italic)
        self.add_card_ui.underline_button.clicked.connect(self.format_text_underline)
        self.add_card_ui.font_color_button.clicked.connect(self.set_font_color)
        self.add_card_ui.highlight_button.clicked.connect(self.set_text_highlight)
        self.add_card_ui.bullete_button.clicked.connect(self.insert_bullet_point)
        self.add_card_ui.numbered_buttton.clicked.connect(self.insert_numbered_bullet_point)
        self.add_card_ui.left_align_button.clicked.connect(lambda: self.set_text_alignment(Qt.AlignLeft))
        self.add_card_ui.right_align_button.clicked.connect(lambda: self.set_text_alignment(Qt.AlignRight))
        self.add_card_ui.center_align_button.clicked.connect(lambda: self.set_text_alignment(Qt.AlignCenter))

        self.add_card_ui.font_size_spin.valueChanged.connect(self.set_font_size)
        self.add_card_ui.font_size_spin.setRange(1, 44)# Set a reasonable range for font size
        self.add_card_ui.font_size_spin.setValue(10)# Set default font size
        self.add_card_ui.font_size_spin.valueChanged.connect(self.set_font_size)
        self.add_card_ui.font_style_combobox.currentFontChanged.connect(self.set_font_style)
        
        self.imgSelect_ui.select_image_button.clicked.connect(self.Insert_image_in_Label)
        # Painter Variables 



    #insert image in label
    def Insert_image_in_Label(self):
        file_name,_= QFileDialog.getOpenFileName(self,"Select Image","C:\\Users\\Swayam\\OneDrive\\Pictures","All Files (*);; PNG Files(*.png);;JPG Files (*.jpg)")
        if file_name:
            #Open Image
            self.pixmap = QPixmap(file_name)
            if self.pixmap.isNull():
                print(f"Error: Unable to load image from path: {file_name}")
            else:
                # Add Image to Label
                self.imgEdit_ui.image_label.setPixmap(self.pixmap)
            self.image_edit_window.show()

     #save image    
    
    #save image
    def save_image(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.bmp);;All Files (*)")

        if file_name:
            self.imgEdit_ui.image_label.pixmap().save(file_name)

    # Return To Deck List from any screen
    def Desks(self):
        pass

    #Open New Add Flash card window 
    def Add_FlashCard(self):
        #self.Toggle_dark_mode(self)
        # self.add_card_ui =Ui_AddFlashCard()
        # self.add_card_ui.setupUi(self.add_window)
        self.add_window.show()

    #Open Stat window
    def Stats(self):
        pass


    ######################## Deck Handeling Functions ########################

    # toggle mode
    def Toggle_dark_mode(self,dark_mode):
        if dark_mode:
            self.setStyleSheet("QMainWindow { background-color: #222; color: #FFF; }"
                                "QLabel { color: #FFF; }"
                                "QRadioButton { color: #FFF; }"
                                "QPushButton {  background-color: #333; color: #FFF; }"
                                "QFrame {  background-color: #333; color: #FFF; }"
                                "QListWidget{  background-color: #333; color: #FFF;border: 1px solid #222; }"
                                "QMenuBar{ background-color: #333; color: #FFF;}"
                                "QInputDialog{ background-color: #333; color: #FFF;}"
                                "QLineEdit{ background-color: #333; color: #FFF;}"
                                "QMessageBox{ background-color: #333; color: #FFF;}"
                                "QStatusBar{ background-color: #333; color: #FFF;}"
                                "QAction{ background-color: #333; color: #FFF;}"
                                "QGroupBox{ background-color: #333; color: #FFF;}"

                                ''' QMenuBar::item { background-color: #333; color: #FFF; }
                                    QMenuBar::item::selected { background-color: #555; color: #FFF; }
                                    QMenuBar::item::!active { background-color: #333; color: #FFF; }
                                    QMenu { background-color: #333; color: #FFF; }
                                    QMenu::item { background-color: #333; color: #FFF; }
                                    QMenu::item::selected { background-color: #555; color: #FFF; }
                                    QMenu::item::!active { background-color: #333; color: #FFF; }
                                    
                                    
                                        '''
                
                                )
            self.add_window.setStyleSheet("QMainWindow { background-color: #222; color: #FFF; }"
                                "QLabel { color: #FFF; }"
                                "QRadioButton { color: #FFF; }"
                                "QPushButton {  background-color: #333; color: #FFF; }"
                                "QFrame {  background-color: #333; color: #FFF; }"
                                "QListWidget{  background-color: #333; color: #FFF;border: 1px solid #222; }"
                                "QMenuBar{ background-color: #333; color: #FFF;}"
                                "QInputDialog{ background-color: #333; color: #FFF;}"
                                "QLineEdit{ background-color: #333; color: #FFF;}"
                                "QMessageBox{ background-color: #333; color: #FFF;}"
                                "QStatusBar{ background-color: #333; color: #FFF;}"
                                "QAction{ background-color: #333; color: #FFF;}"
                                "QGroupBox{ background-color: #333; color: #FFF;border: 1px solid #222;}"

                                ''' QMenuBar::item { background-color: #333; color: #FFF; }
                                    QMenuBar::item::selected { background-color: #555; color: #FFF; }
                                    QMenuBar::item::!active { background-color: #333; color: #FFF; }
                                    QMenu { background-color: #333; color: #FFF; }
                                    QMenu::item { background-color: #333; color: #FFF; }
                                    QMenu::item::selected { background-color: #555; color: #FFF; }
                                    QMenu::item::!active { background-color: #333; color: #FFF; }
                                    
                                        ''')
            self.image_select_window.setStyleSheet("QMainWindow { background-color: #222; color: #FFF; }"
                                "QLabel { color: #FFF; }"
                                "QRadioButton { color: #FFF; }"
                                "QPushButton {  background-color: #333; color: #FFF; }"
                                "QFrame {  background-color: #333; color: #FFF; }"
                                "QListWidget{  background-color: #333; color: #FFF;border: 1px solid #222; }"
                                "QMenuBar{ background-color: #333; color: #FFF;}"
                                "QInputDialog{ background-color: #333; color: #FFF;}"
                                "QLineEdit{ background-color: #333; color: #FFF;}"
                                "QMessageBox{ background-color: #333; color: #FFF;}"
                                "QStatusBar{ background-color: #333; color: #FFF;}"
                                "QAction{ background-color: #333; color: #FFF;}"
                                "QGroupBox{ background-color: #333; color: #FFF;border: 1px solid #222;}"

                                ''' QMenuBar::item { background-color: #333; color: #FFF; }
                                    QMenuBar::item::selected { background-color: #555; color: #FFF; }
                                    QMenuBar::item::!active { background-color: #333; color: #FFF; }
                                    QMenu { background-color: #333; color: #FFF; }
                                    QMenu::item { background-color: #333; color: #FFF; }
                                    QMenu::item::selected { background-color: #555; color: #FFF; }
                                    QMenu::item::!active { background-color: #333; color: #FFF; }
                                    
                                        '''
                                )
            self.image_edit_window.setStyleSheet("QMainWindow { background-color: #222; color: #FFF; }"
                                "QLabel { color: #FFF; }"
                                "QRadioButton { color: #FFF; }"
                                "QPushButton {  background-color: #333; color: #FFF; }"
                                "QFrame {  background-color: #333; color: #FFF; }"
                                "QListWidget{  background-color: #333; color: #FFF;border: 1px solid #222; }"
                                "QMenuBar{ background-color: #333; color: #FFF;}"
                                "QInputDialog{ background-color: #333; color: #FFF;}"
                                "QLineEdit{ background-color: #333; color: #FFF;}"
                                "QMessageBox{ background-color: #333; color: #FFF;}"
                                "QStatusBar{ background-color: #333; color: #FFF;}"
                                "QAction{ background-color: #333; color: #FFF;}"
                                "QGroupBox{ background-color: #333; color: #FFF;border: 1px solid #222;}"

                                ''' QMenuBar::item { background-color: #333; color: #FFF; }
                                    QMenuBar::item::selected { background-color: #555; color: #FFF; }
                                    QMenuBar::item::!active { background-color: #333; color: #FFF; }
                                    QMenu { background-color: #333; color: #FFF; }
                                    QMenu::item { background-color: #333; color: #FFF; }
                                    QMenu::item::selected { background-color: #555; color: #FFF; }
                                    QMenu::item::!active { background-color: #333; color: #FFF; }
                                    
                                        '''
                                )
        else:
            self.setStyleSheet("")
            self.add_window.setStyleSheet("")
            self.image_edit_window.setStyleSheet("")
            self.image_select_window.setStyleSheet("")

    # Load All deck list in list widget from json file
    def Load_Decks(self):
        try:
            with open('data.json','r') as file:
                stored_decks=json.load(file)
                self.deck_list=stored_decks['list_data']
                self.dic=stored_decks['dict_data']
        except FileNotFoundError:
            pass

        self.ui.deck_name_list_widget.addItems(self.deck_list)
        new_list=[]
        learn_list=[]
        due_list=[]
        for name ,list in self.dic.items():
            new_list.append(str(self.dic[name][0]))
            learn_list.append(str(self.dic[name][1]))
            due_list.append(str(self.dic[name][2]))

        print(self.deck_list)
        print(self.dic)
            
        self.ui.new_list_widget.addItems(new_list)
        self.ui.learn_list_widget.addItems(learn_list)
        self.ui.due_list_widget.addItems(due_list)
            

        self.ui.deck_name_list_widget.setCurrentRow(0)
        self.ui.new_list_widget.setCurrentRow(0)
        self.ui.learn_list_widget.setCurrentRow(0)
        self.ui.due_list_widget.setCurrentRow(0)

    # Save Decks in json file
    def save_decks(self):
        with open('data.json', 'w') as file:
            json.dump({'list_data': self.deck_list, 'dict_data': self.dic}, file)
    
    # Create new Deck
    def Add_deck(self):
        curr_index= self.ui.deck_name_list_widget.currentRow()
        text , ok = QInputDialog.getText(self,"Creat Deck","New deck name:")
        if ok and len(text)>0:
            # add decks in text widget also in List and dictionary
            self.ui.deck_name_list_widget.insertItem(curr_index,text) 
            self.deck_list.insert(curr_index,text)
            self.dic[text]=[]

            if len(self.deck_list)%2==0:
                self.ui.new_list_widget.insertItem(curr_index,"0")
                self.dic[text].append(0)
                self.ui.learn_list_widget.insertItem(curr_index,"0") 
                self.dic[text].append(0)
                self.ui.due_list_widget.insertItem(curr_index,"0") 
                self.dic[text].append(0)
            else:
                self.ui.new_list_widget.insertItem(curr_index,"1")
                self.dic[text].append(0)
                self.ui.learn_list_widget.insertItem(curr_index,"1") 
                self.dic[text].append(0)
                self.ui.due_list_widget.insertItem(curr_index,"1") 
                self.dic[text].append(0)

            print(self.dic)
            print(self.deck_list)
    
    #Rename Deck
    def Rename_deck(self):
        curr_index=self.ui.deck_name_list_widget.currentRow()
        deck=self.ui.deck_name_list_widget.item(curr_index) # gives entry at index not text 

        if deck is not None:
            text , ok = QInputDialog.getText(self,"Rename Deck","Edit deck name:",QLineEdit.Normal,deck.text())
            if ok and text is not None:
                #change in list and dic
                oldText=deck.text()
                index=self.deck_list.index(oldText)
                self.dic[text]=self.dic.pop(oldText)
                if index!=ValueError:
                    self.deck_list[index]=text
                #change in list widget 
                deck.setText(text)

        print(self.deck_list)
        print(self.dic)

    #Remove Deck from List and data base
    def Remove_deck(self):
        curr_index=self.ui.deck_name_list_widget.currentRow()
        deck=self.ui.deck_name_list_widget.item(curr_index)

        if deck is not None:
            question=QMessageBox.question(self,"Remove Deck",f"Do you want to delete {deck.text()} Deck?" ,QMessageBox.Yes | QMessageBox.No)
            if question == QMessageBox.Yes:

                #remove from List Widget and from deck list and dic
                text = self.ui.deck_name_list_widget.takeItem(curr_index)
                n=self.ui.new_list_widget.takeItem(curr_index)
                l=self.ui.learn_list_widget.takeItem(curr_index)
                d=self.ui.due_list_widget.takeItem(curr_index)
                del n,l,d
                oldText=deck.text()
                index=self.deck_list.index(oldText)
                del self.dic[oldText]
                if index!=ValueError:
                    del self.deck_list[index]
                del text

        print(self.deck_list)
        print(self.dic)
 
    #Sort List entry acrding to Name
    def Sort_deck(self):
        self.ui.deck_name_list_widget.sortItems()
        self.deck_list.sort()

        count= self.ui.deck_name_list_widget.count()
        for i in range(count):
            deck=self.ui.deck_name_list_widget.item(i).text()
            n=self.ui.new_list_widget.item(i)
            n.setText(str(self.dic[deck][0]))
            l=self.ui.learn_list_widget.item(i)
            l.setText(str(self.dic[deck][0]))
            d=self.ui.due_list_widget.item(i)
            d.setText(str(self.dic[deck][0]))

    #exit programm
    def exit(self):
        question = QMessageBox.question(self,"Quit","Do you want to quit ?",QMessageBox.Yes|QMessageBox.No)
        if question==QMessageBox.Yes:
            quit()
    
    #Move one up any selected deck
    def Move_up_deck(self):
        curr_index=self.ui.deck_name_list_widget.currentRow()

        deck=self.ui.deck_name_list_widget.item(curr_index)
        n=self.ui.new_list_widget.item(curr_index)
        l=self.ui.learn_list_widget.item(curr_index)
        d=self.ui.due_list_widget.item(curr_index)

        if curr_index>=1:
            up_index=curr_index-1
            upDeck=self.ui.deck_name_list_widget.item(up_index)
            un=self.ui.new_list_widget.item(up_index)
            ul=self.ui.learn_list_widget.item(up_index)
            ud=self.ui.due_list_widget.item(up_index)

            curr_text=deck.text()
            nc=n.text()
            lc=l.text()
            dc=d.text()
            up_text=upDeck.text()
            unc=un.text()
            ulc=ul.text()
            udc=ud.text()
            
            deck.setText(up_text)
            n.setText(unc)
            l.setText(ulc)
            d.setText(udc)

            upDeck.setText(curr_text)
            un.setText(nc)
            ul.setText(lc)
            ud.setText(dc)

    #Move one down any selected deck
    def Move_down_deck(self):
        curr_index=self.ui.deck_name_list_widget.currentRow()

        deck=self.ui.deck_name_list_widget.item(curr_index)
        n=self.ui.new_list_widget.item(curr_index)
        l=self.ui.learn_list_widget.item(curr_index)
        d=self.ui.due_list_widget.item(curr_index)

        if curr_index<=self.ui.deck_name_list_widget.count()-2:
            up_index=curr_index+1
            upDeck=self.ui.deck_name_list_widget.item(up_index)
            un=self.ui.new_list_widget.item(up_index)
            ul=self.ui.learn_list_widget.item(up_index)
            ud=self.ui.due_list_widget.item(up_index)

            curr_text=deck.text()
            nc=n.text()
            lc=l.text()
            dc=d.text()
            up_text=upDeck.text()
            unc=un.text()
            ulc=ul.text()
            udc=ud.text()
            
            deck.setText(up_text)
            n.setText(unc)
            l.setText(ulc)
            d.setText(udc)

            upDeck.setText(curr_text)
            un.setText(nc)
            ul.setText(lc)
            ud.setText(dc)


    ######################## ToolBox Functions ########################

    # Bold Sleceted Text
    def format_text_bold(self):
        cursor = self.add_card_ui.front_text.textCursor()
        current_format = cursor.charFormat()
        new_format = QTextCharFormat(current_format)

        # Toggle between making text bold and removing bold formatting
        if current_format.fontWeight() == QFont.Bold:
            new_format.setFontWeight(QFont.Normal)
        else:
            new_format.setFontWeight(QFont.Bold)

        # Explicitly set the format to ensure toggling
        self.apply_formatting(new_format)

    # Italic Sleceted Text
    def format_text_italic(self):
        cursor= self.add_card_ui.front_text.textCursor()
        current_format = cursor.charFormat()
        new_format = QTextCharFormat(current_format)
        new_format.setFontItalic(not current_format.fontItalic())
        self.apply_formatting(new_format)
    
    # UnderLine Sleceted Text
    def format_text_underline(self):
        cursor = self.add_card_ui.front_text.textCursor()
        current_format=cursor.charFormat()
        new_format = QTextCharFormat(current_format)
        new_format.setUnderlineStyle(not current_format.fontUnderline())
        self.apply_formatting(new_format)
    
    # set font size that is in spin box
    def set_font_style(self, font):
        cursor = self.add_card_ui.front_text.textCursor()
        current_format=cursor.charFormat()
        new_format = QTextCharFormat(current_format)
        new_format.setFont(font)
        self.apply_formatting(new_format)

    # set font style that is in font combobox 
    def set_font_size(self, size):
        cursor = self.add_card_ui.front_text.textCursor()
        current_format=cursor.charFormat()
        new_format = QTextCharFormat(current_format)
        new_format.setFontPointSize(size)
        self.apply_formatting(new_format)

    # Change Font color of Sleceted Text
    def set_font_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            cursor= self.add_card_ui.front_text.textCursor()
            current_format = cursor.charFormat()
            new_format = QTextCharFormat(current_format)
            new_format.setForeground(color)
            self.apply_formatting(new_format)
    
    # Change Background Color of Sleceted Text
    def set_text_highlight(self):
        color = QColorDialog.getColor()
        if color.isValid():
            cursor= self.add_card_ui.front_text.textCursor()
            current_format = cursor.charFormat()
            new_format = QTextCharFormat(current_format)
            new_format.setBackground(color)
            self.apply_formatting(new_format)

    def apply_formatting(self, text_format):
        cursor = self.add_card_ui.front_text.textCursor()
        if not cursor.hasSelection():
            return
        cursor.mergeCharFormat(text_format)
    
    #Inser Bullet Point in text
    def insert_bullet_point(self):
        cursor = self.add_card_ui.front_text.textCursor()
        cursor.insertList(QTextListFormat.ListDisc)
    
    # Insert Numbered bullet Points Text
    def insert_numbered_bullet_point(self):
        cursor = self.add_card_ui.front_text.textCursor()
        cursor.insertList(QTextListFormat.ListDecimal)

    # set alignment of text in TextWidget
    def set_text_alignment(self, alignment):
        cursor = self.add_card_ui.front_text.textCursor()
        block_format = cursor.blockFormat()
        block_format.setAlignment(alignment)
        cursor.setBlockFormat(block_format)
    


    #save data when close event accource
    def closeEvent(self, event):
        self.save_decks()
        event.accept()
    
   
def window():
    app = QApplication(sys.argv)
    win = FlashCardApp()
    win.show()
    sys.exit(app.exec_())

window()


