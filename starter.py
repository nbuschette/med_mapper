from tkinter import *
from tkinter import filedialog, messagebox
import rxnorm_api as ap
import csv
import threading

root = Tk()
root.configure(bg="gray")

class easy:
    def __init__(self, master):
        master.minsize(width=100, height=200)
        self.master = master
        #Title
        master.title("Produce RXCUI and NDC Information from Medication Names")
        

        #Information
        self.label2 = Label(master,bg="gray", text="Uploaded File must be a CSV with medication names in seperate rows on column A with no Header.")
        self.label2.grid(row=1, column=2)

        #Button
        self.start_button = Button(master, text="Create Files", command=self.thread, width = 25)
        self.start_button.grid(row=3, column=2)
        
    #Method that reads in CSV, calls API, and outputs RXCUI and NDC CSV files
    def start(self):
        try:
            #hide button while running
            self.start_button.grid_forget()
            self.label3 = Label(self.master,bg="gray", text="Processing...")
            self.label3.grid(row=3, column=2)
            root.update_idletasks()
            #Create empty objects
            med_list = []
            rxcui_list = []
            message = []
            #Get CSV location
            messagebox.showinfo("Okay", "Pick CSV File with Medication Names")
            path = filedialog.askopenfilename(title="Pick CSV File")
            #Get output location
            messagebox.showinfo("Okay", "Pick Location to Save Output Files")
            path_out = filedialog.askdirectory(title="Pick Location to Save Output Files")
            #open CSV
            with open(path) as path_read:
                reader = csv.reader(path_read)
                #loop through rows and grab column A
                for side, row in enumerate(reader):
                    #show which med is being checked
                    self.label3.config(text='Processing '+str(row[0])+'...')
                    root.update_idletasks()
                    #remove only take text prior to ' ('
                    #run through API
                    cui_dict = ap.make_med_data(row[0].split(' (')[0])
                    #create list with med name as index and rxcuis appended
                    if len(list(cui_dict.keys())) == 0:
                        message.append(row[0])
                    med_list.append([row[0]]+ list(cui_dict.keys()))
                    #loop through rxcuis
                    for cui, ndc in cui_dict.items():
                        #create list with rxcui as index and ndcs appended
                        rxcui_list.append([cui]+ndc)
            #update label
            self.label3.config(text='Saving Files...')
            root.update_idletasks()
            #Create and save NDC file-will overwrite
            with open(path_out+'/NDC.csv', 'w', newline="") as file:
                writer = csv.writer(file)#, delimiter=',')
                for i in rxcui_list:
                    writer.writerow(i)
            #Create and save RXCUI file-will overwrite
            with open(path_out+'/RXCUI.csv', 'w', newline="") as file2:
                writer2 = csv.writer(file2)#, delimiter=',')
                for i2 in med_list:
                    writer2.writerow(i2)
                    
            #update label
            self.label3.grid_forget()
            #show button when complete
            self.start_button.grid(row=3, column=2)
            root.update_idletasks()
            #Give success message
            messsage = ', '.join(message)
            messagebox.showinfo("Okay", "File Creations Complete.  Errors:"+str(messsage))
        except Exception as e:
            #update label
            self.label3.grid_forget()
            #show button when complete
            self.start_button.grid(row=3, column=2)
            root.update_idletasks()
            #Give success message
            messagebox.showinfo("Okay", "Error: "+str(e))

    def thread(self):#allows GUI to update accordingly
        threading.Thread(target=self.start).start()

my_gui = easy(root)
root.mainloop()