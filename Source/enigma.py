import random
import pygame
import argparse
import pyperclip
from os import startfile, getcwd
parser = argparse.ArgumentParser()
def derangement(lst):
    n = len(lst)
    while True:
        result = list(range(n))
        random.shuffle(result)
        if all(result[i] != i for i in range(n)):
            break
    return [lst[i] for i in result]
class Enigma_Machine():
    def __init__(self,input_seed=None) -> None:
        self.backend = self.Enigma_Backend(self,input_seed)
        self.display = self.Enigma_Display(self)
        print("Starting ENIGMA with seed:", self.get_seed())
        self.display.main_loop()
    def get_seed(self):
        return self.backend.seed
    def reset(self):
        self.backend.parse_seed(self.get_seed())
        self.display.set_rotors(self.get_seed())
    def help(self):
        help_text = """ENIGMA HELP SECTION (see the README.txt for more information):
        - F1: Used to display help information (this section)
        - Enter: used to reset the enigma machine back to its default settings, as the machine's seed describes. This is effectively resetting it to how it was when the program was launched.
        - Escape: the escape key will close the program.
        - Tab: the tab key can be used to copy the current seed to the clipboard, this action should be displayed by the UI by the seed flashing white."""
        help_file_path = "enigma_help.txt"
        help_file_w = open(help_file_path, "w")
        help_file_w.write(help_text)
        help_file_w.close()
        startfile(getcwd()+"\\"+help_file_path, 'open')
        print(help_text)
    class Enigma_Backend():
        def __init__(self,parent,input_seed=None) -> None:
            self.debug_on = False
            self.parent = parent
            self._alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            ROTOR_CROSSWIRE1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
            ROTOR_CROSSWIRE2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
            ROTOR_CROSSWIRE3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
            ROTOR_CROSSWIRE4 = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
            ROTOR_CROSSWIRE5 = "VZBRGITYUPSDNHLXAWMJQOFECK"
            self.REFLECTOR = "APBNCSDKEVFLGRHOIYJTKDLFMUNBOHPAQXRGSCTJUMVEWZXQYIZW"
            self.rotors = [ROTOR_CROSSWIRE1,ROTOR_CROSSWIRE2,ROTOR_CROSSWIRE3,ROTOR_CROSSWIRE4,ROTOR_CROSSWIRE5]
            self.rotor_settings = ""
            if input_seed == None:
                self.seed = self._generate_seed()
            else:
                self.parse_seed(input_seed)
        def parse_seed(self,seed):
            self.seed = seed
            self.rotor_settings = seed[0:6]
            dissolved_plug = seed[6:]
            self.plugboard = "".join([self._alphabet[i]+dissolved_plug[i] for i in range(0,len(dissolved_plug))])
        def _debug(self,*debug_text):
            if self.debug_on:
                print("ENIGMA_DEBUG:",*debug_text)
        def _generate_seed(self):
            key = ""
            #plugboard
            alph = self._alphabet.copy()
            random.shuffle(alph)
            half_size = len(alph)//2
            half1 = alph[0:half_size]
            half2 = alph[half_size:]
            full = {}
            for i in range(0,half_size):
                full[half1[i]] = half2[i]
                full[half2[i]] = half1[i]
            for letter in self._alphabet:
                key += letter+full[letter]
            self.plugboard = key
            dissolved_key = "".join([key[i] for i in range(0,len(key)) if i % 2 == 1])
            key = dissolved_key
            #rotors
            rotor_index = [x for x in range(0,len(self.rotors))]
            random.shuffle(rotor_index)
            for i in rotor_index:
                self.rotor_settings = self.rotor_settings + str(i) + str(random.choice(self._alphabet))
            key = self.rotor_settings+key
            return key
        def _get_reversed_wiring(self,wiring):
            reverse = ["" for x in range(0,26)]
            for i, letter in enumerate(wiring):
                reverse[self._alphabet.index(letter)] = self._alphabet[i]
            return "".join(reverse)           
        def _step_rotors(self):
            new_settings = [x for x in self.rotor_settings]
            def step(rotor):
                cycle = False
                rotor_index = (self._alphabet.index(rotor[1])+1)
                if rotor_index >= 26:
                    rotor_index = rotor_index%26
                    cycle = True
                return rotor[0]+self._alphabet[rotor_index], cycle
            rotor1 = step(self.rotor_settings[0:2])
            new_settings[0],new_settings[1] = rotor1[0][0],rotor1[0][1]
            if rotor1[1]:
                rotor2 = step(self.rotor_settings[2:4])
                new_settings[2],new_settings[3] = rotor2[0][0],rotor2[0][1]
                if rotor2[1]:
                    rotor3 = step(self.rotor_settings[4:6])
                    new_settings[4],new_settings[5] = rotor3[0][0],rotor3[0][1]
            self.rotor_settings = "".join(new_settings)
            self.parent.display.set_rotors(self.rotor_settings)
        def _fail(self,invalid_char):
            raise Exception("Invalid string entered: '"+invalid_char+"' not found in: ["+"".join(self._alphabet)+"]")
        def _plug(self,letter):
            return self.plugboard[((self._alphabet.index(letter)*2)+1%26)]
        def _through_rotor(self,letter,rotor,setting):
            offset = self._alphabet.index(setting)
            letter_index = self._alphabet.index(letter)
            input_index = (letter_index + offset) % 26
            substituted_letter = rotor[input_index]
            output_index = self._alphabet.index(substituted_letter)
            result_index = (output_index - offset + 26) % 26
            return self._alphabet[result_index]
        def _reflect(self,letter):
            return self.REFLECTOR[((self._alphabet.index(letter)*2)+1%26)]
        def _get_enciphered_letter(self, letter):
            self._debug(letter,"(input)")
            letter = self._plug(letter)
            self._debug(letter,"(plugged)")
            for s in range(0,len(self.rotor_settings)-1): #rotor settings are in pairs rotor_index+shift_value
                if s%2 == 0:
                    rotor_index = self.rotor_settings[s]
                    setting = self.rotor_settings[s+1]
                    rotor = self.rotors[int(rotor_index)]
                    letter = self._through_rotor(letter,rotor,setting)
                    self._debug(letter,"(rotor"+rotor_index+")")
            letter = self._reflect(letter)
            self._debug(letter, "(reflected)")
            for s in reversed(range(0,len(self.rotor_settings)-1)): #rotor settings are in pairs rotor_index+shift_value
                if s%2 == 0:
                    rotor_index = self.rotor_settings[s]
                    setting = self.rotor_settings[s+1]
                    rotor = self._get_reversed_wiring(self.rotors[int(rotor_index)])
                    letter = self._through_rotor(letter,rotor,setting)
                    self._debug(letter,"(reverse rotor"+rotor_index+")")
            letter = self._plug(letter)
            self._debug(letter,"(plugged2)")
            return letter
        def encipher(self, letter):
            letter = letter.upper()
            if not letter in self._alphabet:
                self._fail(letter)
            letter = self._get_enciphered_letter(letter)
            self._step_rotors()
            return letter
    class Enigma_Display():
        def __init__(self,parent) -> None:
            self.parent = parent
            self.ASSET_DIR = "ASSETS/"
            self.KEY_ON_DIR = self.ASSET_DIR+"KEYS/ON"
            self.KEY_OFF_DIR = self.ASSET_DIR+"KEYS/OFF"
            self.LAMP_ON_DIR = self.ASSET_DIR+"LAMPS/ON"
            self.LAMP_OFF_DIR = self.ASSET_DIR+"LAMPS/OFF"
            self.ENIGMA_BACKGROUND = pygame.image.load(self.ASSET_DIR+"ENIGMA_BACKGROUND.png")
            self.ROTOR = pygame.image.load(self.ASSET_DIR+"ROTOR.png")
            self.ROTOR_TURNING = pygame.image.load(self.ASSET_DIR+"ROTOR_TURNING.png")
            self.FONT = "Arial"
            self.rotor_images = [self.ROTOR,self.ROTOR,self.ROTOR]
            self.keys_pressed = []
            self.key_to_lamp = {}
            self.lamps_on = []
            self.rotor_display = ["A","A","A"]
            pygame.init()
            pygame.display.set_caption("ENIGMA")
            window_icon = pygame.image.load(self.ASSET_DIR+"icon.ico")
            pygame.display.set_icon(window_icon)
            self.screen = pygame.display.set_mode((854, 480),pygame.RESIZABLE)
            self.clock = pygame.time.Clock()
            self.running = True
            self.displaying_seed_coppy = False
            self.seed_coppy = False
            self.rotors_changed = [False,False,False]
            self.tick_speed = 40
            self.BG_COLOUR = (15, 15, 15)
            self.set_rotors(self.parent.backend.rotor_settings)
        def get_keydisplay(self,directory,activated,key_sinking=True):
            global keyboard
            row_max_size = len(max(keyboard,key=len))
            spacing = (40,10)
            key_size = (80,80)
            if key_sinking:
                key_sink = spacing[1]/2
            else:
                key_sink = 0
            total_size = ((spacing[0]*row_max_size-1)+(key_size[0]*row_max_size),(spacing[1]*(len(keyboard)-1))+(key_size[1]*len(keyboard))+key_sink)
            surface = pygame.surface.Surface(total_size,pygame.SRCALPHA)
            for row in range(0,len(keyboard)):
                for col in range(0,len(keyboard[row])):
                    key = keyboard[row][col]
                    if key in activated:
                        key_image = pygame.image.load(directory+"/ON/"+key+".png")
                        key_position = (col*(spacing[0]+key_size[0]),row*(spacing[1]+key_size[1])+key_sink)
                    else:
                        key_image = pygame.image.load(directory+"/OFF/"+key+".png")
                        key_position = (col*(spacing[0]+key_size[0]),row*(spacing[1]+key_size[1]))
                    row_size = ((len(keyboard[row])-1)*spacing[0])+(len(keyboard[row])*key_size[0])
                    offset = ((total_size[0]/2)-(row_size/2))*0.6
                    surface.blit(key_image,(key_position[0]+offset,key_position[1]))
            return surface   
        def set_rotors(self,rotor_settings):
            old_display = self.rotor_display.copy()
            self.rotor_display = [rotor_settings[5],rotor_settings[3],rotor_settings[1]]
            self.rotors_changed = [self.rotor_display[0]!=old_display[0],self.rotor_display[1]!=old_display[1],self.rotor_display[2]!=old_display[2]]
            self.since_rotors_changed = 0
        def get_rotor_display(self):
            label_spacing = 102
            label_width = 20
            label_surface = pygame.surface.Surface(((label_spacing*(len(self.rotor_display)-1))+(label_width*len(self.rotor_display)),100),pygame.SRCALPHA)
            for rotor in range(0,len(self.rotor_display)):
                label_text = self.rotor_display[rotor]
                label_font = pygame.font.SysFont(self.FONT,25,True,False)
                label = label_font.render(label_text, False, (150, 150, 150))
                label_surface.blit(label,((label_spacing+label_width)*rotor,0))
            return label_surface
        def get_rotors(self):
            rotor_size = (48,240)
            rotor_spacing = 72
            rotor_surface = pygame.surface.Surface(((rotor_size[0]*2.5)+(rotor_spacing*2), rotor_size[1]),pygame.SRCALPHA)
            for i in range(0,len(self.rotor_images)):
                rotor_image = self.rotor_images[i]
                rotor_pos = ((rotor_size[0]+rotor_spacing)*i,0)
                rotor_surface.blit(rotor_image,rotor_pos)
            return rotor_surface
        def get_seed_label(self,active):
            label_font = pygame.font.SysFont(self.FONT,20,True,False)
            seed_unactive = (145, 90, 70)
            seed_active = (255, 255, 255)
            if active:
                seed_colour = seed_active
                self.displaying_seed_coppy = False
                self.seed_coppy = True
            else:
                seed_colour = seed_unactive
                self.seed_coppy = False
            label = label_font.render(self.parent.get_seed(), False, seed_colour)
            return label
        def display(self):
            self.screen.fill(self.BG_COLOUR)
            main_surface_raw = pygame.surface.Surface((1435,1125))
            main_surface_raw.blit(self.ENIGMA_BACKGROUND,(0,0))
            main_surface_raw.blit(self.get_keydisplay(self.ASSET_DIR+"LAMPS",self.lamps_on,False),(160,360))
            main_surface_raw.blit(self.get_keydisplay(self.ASSET_DIR+"KEYS",self.keys_pressed,True),(160,750))
            main_surface_raw.blit(self.get_rotor_display(),(535,200))
            main_surface_raw.blit(self.get_rotors(),(585,95))
            seed_label = self.get_seed_label(self.displaying_seed_coppy)
            main_surface_raw.blit(seed_label,((1435/2)-(seed_label.get_width()/2),15))
            size_multiplier = min((self.screen.get_width()/main_surface_raw.get_width()),(self.screen.get_height()/main_surface_raw.get_height()))
            main_surface = pygame.transform.scale(main_surface_raw, (main_surface_raw.get_width()*size_multiplier,main_surface_raw.get_height()*size_multiplier))
            x, y = (self.screen.get_width()/2)-(main_surface.get_width()/2), (self.screen.get_height()/2)-(main_surface.get_height()/2)
            self.screen.blit(main_surface,(x,y))
            pygame.display.update()
        def main_loop(self):
            self.display()
            while self.running:
                needs_update = False
                if self.displaying_seed_coppy != self.seed_coppy:
                    needs_update = True
                for i in range(0,len(self.rotor_images)):
                    image = self.rotor_images[i]
                    turning = self.rotors_changed[i]
                    if turning and image != self.ROTOR_TURNING:
                        needs_update = True
                    elif not turning and image != self.ROTOR:
                        needs_update = True
                for i in range(0,len(self.rotors_changed)):
                    if self.rotors_changed[i]:
                        self.rotor_images[i] = self.ROTOR_TURNING
                        self.rotors_changed[i] = False
                    else:
                        self.rotor_images[i] = self.ROTOR
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN:
                        key = str(pygame.key.name(event.key)).upper()
                        if key in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
                            self.keys_pressed.append(key)
                            cipher_letter = self.parent.backend.encipher(key)
                            self.key_to_lamp[key] = cipher_letter
                            self.lamps_on.append(cipher_letter)
                            needs_update = True
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                        if event.key == pygame.K_TAB:
                            self.displaying_seed_coppy = True
                            pyperclip.copy(self.parent.get_seed())
                            print("SEED COPPIED TO CLIPBOARD")
                        if event.key == pygame.K_RETURN:
                            self.parent.reset()
                        if event.key == pygame.K_F1:
                            self.parent.help()
                    if event.type == pygame.KEYUP:
                        key = str(pygame.key.name(event.key)).upper()
                        if key in self.keys_pressed:
                            cipher_letter = self.key_to_lamp.pop(key)
                            self.lamps_on.remove(cipher_letter)
                            self.keys_pressed = list(filter(lambda a: a != key,self.keys_pressed))
                        needs_update = True
                    if event.type == pygame.VIDEORESIZE:
                        needs_update = True
                if needs_update:
                    self.display()
                self.clock.tick(self.tick_speed)
            pygame.quit()
parser.add_argument("--seed")
parser.add_argument("--historical_keyboard")
seed = vars(parser.parse_args())["seed"]
historical_keyboard = vars(parser.parse_args())["historical_keyboard"]=="True"
if historical_keyboard:
    keyboard = [["Q","W","E","R","T","Z","U","I","O"],["A","S","D","F","G","H","J","K"],["P","Y","X","C","V","B","N","M","L"]]
else:
    keyboard = [["Q","W","E","R","T","Y","U","I","O","P"],["A","S","D","F","G","H","J","K","L"],["Z","X","C","V","B","N","M"]]


print(seed)
e = Enigma_Machine(seed)
