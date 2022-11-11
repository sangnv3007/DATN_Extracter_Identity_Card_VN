from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from turtle import color, distance
from PIL import Image, ImageTk
from tkinter import filedialog as fd
import math
from cv2 import ellipse
from matplotlib.pyplot import text
from process import ReturnInfoCard, compare
import json
import time
from numpy import pad

def uploadF():
    global pathFront
    filetypes = (
        ('Image Files', '*.jpg *.jpeg *.bmp *.png *.webp'),
        ('All files', '*.*')
    )
    filenameF = fd.askopenfilename(
        title='Chọn ảnh mặt trước CCCD',
        initialdir='/',
        filetypes=filetypes)
    imgFront = ImageTk.PhotoImage(Image.open(filenameF).resize((400, 270)))
    lb_photo_page1.configure(image=imgFront)
    lb_photo_page1.image = imgFront
    bt_uploadF.configure(text="Chụp/ Tải lại",  bg="white", fg='black')
    bt_uploadF.place(relx=0.3, width=250, anchor=CENTER)
    bt_continueF.place(relx=0.7, rely=0.7, anchor=CENTER, width=250)
    pathFront = filenameF

def uploadB():
    global pathBack
    filetypes = (
        ('Image Files', '*.jpg *.jpeg *.bmp *.png *.webp'),
        ('All files', '*.*')
    )
    filenameB = fd.askopenfilename(
        title='Chọn ảnh mặt sau CCCD',
        initialdir='/',
        filetypes=filetypes)
    imgBack = ImageTk.PhotoImage(Image.open(filenameB).resize((400, 270)))
    lb_photo_page2.configure(image=imgBack)
    lb_photo_page2.image = imgBack
    bt_uploadB.configure(text="Chụp/ Tải lại",  bg="white", fg='black')
    bt_uploadB.place(relx=0.3, width=250, anchor=CENTER)
    bt_continueB.place(relx=0.7, rely=0.7, anchor=CENTER, width=250)
    label_return_page1.place(relx=0.5, rely=0.8, anchor=CENTER)
    pathBack = filenameB

def process():
    global objfront, objback
    process_bar.place(relx=0.5, rely=0.95, anchor=CENTER)
    process_bar['value'] = 0
    process_bar['value'] = 20
    formF.update_idletasks()
    start =  time.time()
    objfront = ReturnInfoCard(pathFront)
    # json_string_F = json.dumps({"errorCode": obj1.errorCode, "errorMessage": obj1.errorMessage,
    #                             "data":[{"id": obj1.id, "name": obj1.name, "dob": obj1.dob,"sex": obj1.sex,
    #                             "nationality": obj1.nationality,"home": obj1.home, "address": obj1.address,
    #                             "doe": obj1.doe,"imageFace": obj1.imageFace, "type": obj1.type}]},ensure_ascii=False).encode('utf8')
    # print(json_string_F.decode())
    objback = ReturnInfoCard(pathBack)
    end = time.time()
    total_time = end - start
    print("Total time: {0} ".format(str(total_time) + " giây..."))
    process_bar['value'] = 60
    formF.update_idletasks()
    process_bar['value'] = 80
    formF.update_idletasks()
    # json_string_B = json.dumps({"errorCode": obj2.errorCode, "errorMessage": obj2.errorMessage,
    #                             "data":[{"features": obj2.features, "issue_date": obj2.issue_date,
    #                             "type": obj2.type}]}, ensure_ascii= False).encode('utf8')
    # print(json_string_B.decode())
    process_bar['value'] = 100
    process_bar.destroy()
    show_frame(page3)

def uploadFace():
    global pathFace
    filetypes = (
        ('Image Files', '*.jpg *.jpeg *.bmp *.png *.webp'),
        ('All files', '*.*')
    )
    filenameFace = fd.askopenfilename(
        title='Chọn ảnh khuôn mặt công dân',
        initialdir='/',
        filetypes=filetypes)
    imgFace = ImageTk.PhotoImage(Image.open(filenameFace).resize((200, 350)))
    label_photo_page3.configure(image=imgFace)
    label_photo_page3.image = imgFace
    bt_uploadFace.configure(text="Chụp/ Tải lại",  bg="white", fg='black')
    bt_uploadFace.place(relx=0.3, width=250, anchor=CENTER)
    bt_continueFace.place(relx=0.7, rely=0.8, anchor=CENTER, width=250)
    pathFace = filenameFace
    label_return_page2.place(relx=0.5, rely=0.9, anchor=CENTER)
def show_frame(frame):
    frame.tkraise()

def res():
    #Update các trường dữ liệu trên form
    res_imageFront= ImageTk.PhotoImage(Image.open(pathFront).resize((250, 200)))
    lb_res_front.configure(image=res_imageFront)
    lb_res_front.image = res_imageFront
    #
    res_imageBack= ImageTk.PhotoImage(Image.open(pathBack).resize((250, 200)))
    lb_res_back.configure(image=res_imageBack)
    lb_res_back.image = res_imageBack
    #
    res_imageFace= ImageTk.PhotoImage(Image.open(pathFace).resize((250, 200)))
    lb_res_face.configure(image=res_imageFace)
    lb_res_face.image = res_imageFace
    #
    face_distance = compare(pathFront, pathFace)
    res_from_distance = face_distance < 0.45
    lb_res_facematch.configure(text=str(res_from_distance)+'('+str(face_distance)+')')
    lb_res_id.configure(text=objfront.id)
    lb_res_name.configure(text=objfront.name)
    lb_res_dob.configure(text=objfront.dob)
    lb_res_sex.configure(text=objfront.sex)
    lb_res_nationality.configure(text=objfront.nationality)
    lb_res_home.configure(text=objfront.home)
    lb_res_address.configure(text=objfront.address)
    lb_res_doe.configure(text=objfront.doe)
    lb_res_features.configure(text=objback.features)
    lb_res_issue_date.configure(text=objback.issue_date)
    show_frame(page4)
# Create formFp
formF = Tk()
formF.title("Chương trình demo eKYC")
formF.geometry("900x700")
formF.rowconfigure(0, weight=1)
formF.columnconfigure(0, weight=1)
#formF.state('zoomed')
#setup page app
page1 = Frame(formF)
page2 = Frame(formF)
page3 = Frame(formF)
page4 = Frame(formF)
for frame in (page1, page2, page3, page4):
    frame.grid(row=0, column=0, sticky='nsew') 
show_frame(page1)
# ======== Page 1(Upload front photo) ========
lb_title_page1 = Label(page1, text="Chụp lại ảnh Thẻ căn cước mặt trước của bạn", font='Times 16 bold')
lb_title_page1.pack(side="top")
lb_notice_page1 = Label(
    page1, text="* Vui lòng sử dụng giấy tờ thật. Hãy đảm bảo ảnh chụp không bị mờ hoặc bóng, thông tin hiển thị rõ ràng, dễ đọc.",
    font='Times 8', fg='red')
lb_notice_page1.place(relx=0.5, rely=0.1, anchor=CENTER)
photoF = PhotoImage(file="cmt.be3f6567.png")
lb_photo_page1 = Label(page1, image=photoF)
lb_photo_page1.place(relx=0.5, rely=0.4, anchor=CENTER)
bt_uploadF = Button(page1, text="Tải ảnh/ Chụp ảnh", font=("Times 16 bold"), bg="blue", fg='white', command=uploadF)
bt_uploadF.place(relx=0.5, rely=0.7, anchor=CENTER, width=600)
bt_continueF = Button(page1, text="Tiếp theo", font=("Times 16 bold"), bg="blue", fg='white', command=lambda: show_frame(page2))
bt_continueF.place(width=0)
# ======== Page 2(Upload back photo) ========
lb_title_page2 = Label(page2, text="Chụp lại ảnh Thẻ căn cước mặt sau của bạn", font='Times 16 bold')
lb_title_page2.pack(side="top")
lb_notice_page2 = Label(
    page2, text="* Vui lòng sử dụng giấy tờ thật. Hãy đảm bảo ảnh chụp không bị mờ hoặc bóng, thông tin hiển thị rõ ràng, dễ đọc.",
    font='Times 8', fg='red')
lb_notice_page2.place(relx=0.5, rely=0.1, anchor=CENTER)
photoB = PhotoImage( file="cmt_back.29611820.png")
lb_photo_page2 = Label(page2, image=photoB)
lb_photo_page2.place(relx=0.5, rely=0.4, anchor=CENTER)
bt_uploadB = Button(page2, text="Tải ảnh/ Chụp ảnh", font=("Times 16 bold"), bg="blue", fg='white', command=uploadB)
bt_uploadB.place(relx=0.5, rely=0.7, anchor=CENTER, width=600)
bt_continueB = Button(page2, text="Tiếp theo", font=("Times 16 bold"), bg="blue", fg='white', command= process)
bt_continueB.place(width=0)
label_return_page1 = Button(page2, text="Quay lại", font=("Times 16 bold"), bg="white", fg='red', command=lambda: show_frame(page1))
process_bar = ttk.Progressbar(page2, orient = HORIZONTAL, length = 400, mode = 'determinate')
# ======== Page 3(Upload Face photo) ========
lb_title_page3 = Label(page3, text="Chụp lại ảnh khuôn mặt của bạn", font='Times 16 bold')
lb_title_page3.pack(side="top")
lb_notice_page3 = Label(
    page3, text="* Vui lòng sử dụng ảnh khuôn mặt thật của bạn. Hãy đảm bảo ảnh chụp không bị mờ hoặc bóng, có thể nhìn rõ khuôn mặt.",
    font='Times 8', fg='red')
lb_notice_page2.place(relx=0.5, rely=0.1, anchor=CENTER)
imgFace = PhotoImage(file="face.c8f1db03.png")
label_photo_page3= Label(page3,image=imgFace)
label_photo_page3.place(relx=0.5, rely=0.4, anchor=CENTER)
bt_uploadFace = Button(page3, text="Tải ảnh/ Chụp ảnh", font=("Times 16 bold"), bg="blue", fg='white', command=uploadFace)
bt_uploadFace.place(relx=0.5, rely=0.8, anchor=CENTER, width=600)
bt_continueFace = Button(page3, text="Tiếp theo", font=("Times 16 bold"), bg="blue", fg='white', command=res)
bt_continueFace.place(width=0)
label_return_page2 = Button(page3, text="Quay lại", font=("Times 16 bold"), bg="white", fg='red', command=lambda: show_frame(page2))

# ======== Page 4(Return result) ========
lb_title_page4 = Label(page4, text="Kết quả xác minh", font='Times 16 bold')
lb_title_page4.pack(side="top")
res_photo_front = ImageTk.PhotoImage(Image.open("cmt.be3f6567.png"))
lb_res_front= Label(page4,image=res_photo_front)
lb_res_front.place(relx=0.2,rely=0.2, anchor=CENTER)
res_photo_back = ImageTk.PhotoImage(Image.open("cmt_back.29611820.png"))
lb_res_back= Label(page4,image=res_photo_back)
lb_res_back.place(relx=0.5, rely=0.2, anchor=CENTER)
res_photo_face = ImageTk.PhotoImage(Image.open("face.c8f1db03.png"))
lb_res_face= Label(page4,image=res_photo_face)
lb_res_face.place(relx=0.8, rely=0.2, anchor=CENTER)
#
lb_show_facematch = Label(page4,text="Face match : ", font='Time 12 bold')
lb_show_facematch.place(rely=0.4,anchor="w")
lb_res_facematch = Label(page4,text="N/A", font='Time 14 bold', fg='green')
lb_res_facematch.place(relx=0.4,rely=0.4,anchor="w")
#
lb_show_id = Label(page4,text="Số CCCD : ", font='Time 12 bold')
lb_show_id.place(rely=0.45,anchor="w")
lb_res_id = Label(page4,text="N/A", font='Time 12')
lb_res_id.place(relx=0.4,rely=0.45,anchor="w")
#
lb_show_name= Label(page4,text="Họ và tên : ", font='Time 12 bold')
lb_show_name.place(rely=0.5,anchor="w")
lb_res_name= Label(page4,text="N/A", font='Time 12')
lb_res_name.place(relx=0.4,rely=0.5,anchor="w")
#
lb_show_dob= Label(page4,text="Ngày sinh : ", font='Time 12 bold')
lb_show_dob.place(rely=0.55,anchor="w")
lb_res_dob= Label(page4,text="N/A", font='Time 12')
lb_res_dob.place(relx=0.4,rely=0.55,anchor="w")
#
lb_show_sex= Label(page4,text="Giới tính : ", font='Time 12 bold')
lb_show_sex.place(rely=0.6,anchor="w")
lb_res_sex= Label(page4,text="N/A", font='Time 12')
lb_res_sex.place(relx=0.4,rely=0.6,anchor="w")
#
lb_show_nationality= Label(page4,text="Quốc tịch : ", font='Time 12 bold')
lb_show_nationality.place(rely=0.65,anchor="w")
lb_res_nationality= Label(page4,text="N/A", font='Time 12')
lb_res_nationality.place(relx=0.4,rely=0.65,anchor="w")
#
lb_show_address= Label(page4,text="Quê quán : ", font='Time 12 bold')
lb_show_address.place(rely=0.7,anchor="w")
lb_res_address= Label(page4,text="N/A", font='Time 12')
lb_res_address.place(relx=0.4,rely=0.7,anchor="w")
#
lb_show_home= Label(page4,text="Nơi thường trú : ", font='Time 12 bold')
lb_show_home.place(rely=0.75,anchor="w")
lb_res_home= Label(page4,text="N/A", font='Time 12')
lb_res_home.place(relx=0.4,rely=0.75,anchor="w")
#
lb_show_doe = Label(page4,text="Ngày hết hạn : ", font='Time 12 bold')
lb_show_doe.place(rely=0.8,anchor="w")
lb_res_doe= Label(page4,text="N/A", font='Time 12')
lb_res_doe.place(relx=0.4,rely=0.8,anchor="w")
#
lb_show_features= Label(page4,text="Đặc điểm nhận dạng : ", font='Time 12 bold')
lb_show_features.place(rely=0.85,anchor="w")
lb_res_features= Label(page4,text="N/A", font='Time 12')
lb_res_features.place(relx=0.4,rely=0.85,anchor="w")
#
lb_show_issue_date = Label(page4,text="Ngày cấp : ", font='Time 12 bold')
lb_show_issue_date.place(rely=0.9,anchor="w")
lb_res_issue_date= Label(page4,text="N/A", font='Time 12')
lb_res_issue_date.place(relx=0.4,rely=0.9,anchor="w")
#
label_return_page = Button(page4, text="Quay lại", font=("Times 16 bold"), bg="white", fg='red', command=lambda: show_frame(page1))
label_return_page.place(relx=0.5, rely=0.95, anchor=CENTER)
formF.mainloop()