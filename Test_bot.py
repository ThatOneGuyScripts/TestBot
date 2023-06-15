import time
import utilities.api.item_ids as ids
import utilities.color as clr
import utilities.random_util as rd
from model.osrs.osrs_bot import OSRSBot
from model.runelite_bot import BotStatus
from utilities.api.morg_http_client import MorgHTTPSocket
from utilities.api.status_socket import StatusSocket
from utilities.geometry import RuneLiteObject
import utilities.ScreenToClient  as stc #comment out if not using remote input
import utilities.RIOmouse as Mouse #comment out if not using rmeote input
import utilities.BackGroundScreenCap as bcp #comment out if not using remote input
import utilities.imagesearch as imsearch
from PIL import Image
import cv2
import os
import threading
import utilities.ocr as ocr





class OSRSTest_Bot(OSRSBot):
    def __init__(self):
        bot_title = "Test Bot"
        description = "This is a test Bot to check functions inside of your osbc/runelite enviorment"
        super().__init__(bot_title=bot_title, description=description)
        self.running_time = 1
        self.Client_Info = None
        self.win_name = None
        self.pid_number = None
        self.Input = "failed to set mouse input"
        self.is_idle = False   
    
        

    def create_options(self):
        self.options_builder.add_slider_option("running_time", "How long to run (minutes)?", 1, 500)
        self.options_builder.add_process_selector("Client_Info")
        self.options_builder.add_checkbox_option("Input","Choose Input Method",["Remote","PAG"])

    def save_options(self, options: dict):
        for option in options:
            if option == "running_time":
                self.running_time = options[option]
            elif option == "Client_Info":
                self.Client_Info = options[option]
                client_info = str(self.Client_Info)
                win_name, pid_number = client_info.split(" : ")
                self.win_name = win_name
                self.pid_number = int(pid_number)
                self.win.window_title = self.win_name
                self.win.window_pid = self.pid_number
                stc.window_title = self.win_name
                Mouse.Mouse.clientpidSet = self.pid_number
                bcp.window_title = self.win_name
                bcp
            elif option == "Input":
                self.Input = options[option]
                if self.Input == ['Remote']:
                    Mouse.Mouse.RemoteInputEnabledSet = True
                elif self.Input == ['PAG']:
                    Mouse.Mouse.RemoteInputEnabledSet = False
                else:
                    self.log_msg(f"Failed to set mouse")  
            else:
                self.log_msg(f"Unknown option: {option}")
                print("Developer: ensure that the option keys are correct, and that options are being unpacked correctly.")
                self.options_set = False
                return
        self.log_msg(f"Running time: {self.running_time} minutes.")
        self.log_msg("Options set successfully.")
        self.log_msg(f"{self.win_name}")
        self.log_msg(f"{self.pid_number}")
        self.log_msg(f"{self.Input}")
        self.options_set = True
        
    
            
    def main_loop(self):

        start_time = time.time()
        end_time = self.running_time * 60
        while time.time() - start_time < end_time:
            # uncomment functions you want to run
           #self.ocr_extract_text_check(self.win.mouseover,ocr.BOLD_12,clr.OFF_WHITE)
           #self.mouse_over_text_check("Walk",clr.OFF_WHITE)
           #self.show_window(self.win.game_view)
           #self.save_window(self.win.game_view,"game_view")
           self.contour_check(self.win.game_view,clr.BLACK)
           time.sleep(0.1)
           
    def ocr_extract_text_check(self,window,font,color):
        #prints ocr to log box
         text = ocr.extract_text(window, font, color)
         self.log_msg(f"{text}")
        
    def mouse_over_text_check(self,text,color):
        #prints detected mouse over text to log box
        if self.mouseover_text(contains=text, color=color):
            self.log_msg(f"{text} found")
        else: 
            self.log_msg(f"{text} not found")
            
    def show_window(self,window):
        #opens a pop up of the given window
        cv2.imshow("x",window.screenshot())
        self.log_msg(f"press key to continue")
        cv2.waitKey(0)
        
    def save_window(self,window,filename):
        #saves a png of the selected window
        cv2.imwrite(f"{filename}.png",window.screenshot())
        self.log_msg(f"press key to continue")
        cv2.waitKey(0)
        
    def contour_check(self,window,color):
        if self.get_all_tagged_in_rect(window,color):
            self.log_msg(f" contour was found")
        else:
            self.log_msg(f"contour was NOT found")
        
                 

    
  
