from tkinter import *
from tkinter import ttk, messagebox
from turtle import color, distance
from PIL import Image, ImageTk, ImageSequence
from tkinter import filedialog as fd
import math
from cv2 import ellipse
from matplotlib.pyplot import text
from process import ReturnInfoCard, compare, face_confidence
import json
import time
import customtkinter


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
    bt_uploadF.configure(text="Chụp/ Tải lại", width=250)
    bt_uploadF.place(relx=0.3, anchor=CENTER)
    bt_continueF.configure(width=250, height=50)
    bt_continueF.place(relx=0.7, rely=0.7, anchor=CENTER)
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
    bt_uploadB.configure(text="Chụp/ Tải lại", width=250)
    bt_uploadB.place(relx=0.3, anchor=CENTER)
    bt_continueB.configure(width=250, height=50)
    bt_continueB.place(relx=0.7, rely=0.7, anchor=CENTER)
    label_return_page1.place(relx=0.5, rely=0.8, anchor=CENTER)
    label_return_page1.configure(height=50)
    pathBack = filenameB


def process():
    global objfront, objback
    process_bar = ttk.Progressbar(
        page2, orient=HORIZONTAL, length=200, mode='determinate')
    process_bar.place(relx=0.5, rely=0.95, anchor=CENTER)
    process_bar['value'] = 0
    process_bar['value'] = 10
    formF.update_idletasks()
    start = time.time()
    process_bar['value'] = 30
    formF.update_idletasks()
    # Check result objfront
    objfront = ReturnInfoCard(pathFront)
    process_bar['value'] = 50
    time.sleep(0.1)
    formF.update_idletasks()
    process_bar['value'] = 80
    formF.update_idletasks()
    objback = ReturnInfoCard(pathBack)
    end = time.time()
    total_time = end - start
    print("Total time: {0} ".format(str(total_time) + " giây..."))
    process_bar['value'] = 100
    formF.update_idletasks()
    time.sleep(0.1)
    process_bar.destroy()
    if (objfront.errorCode != 0 or objfront.type != 'cccd_front'):
        messagebox.showerror('Thông báo', 'Ảnh CCCD mặt trước không hợp lệ')
    elif (objback.errorCode != 0 or objback.type != 'cccd_back'):
        messagebox.showerror('Thông báo', 'Ảnh CCCD mặt sau không hợp lệ')
    else:
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
    bt_uploadFace.configure(text="Chụp/ Tải lại", width=250)
    bt_uploadFace.place(relx=0.3, anchor=CENTER)
    bt_continueFace.place(relx=0.7, rely=0.75, anchor=CENTER)
    bt_continueFace.configure(width=250, height=50)
    label_return_page2.place(relx=0.5, rely=0.85, anchor=CENTER)
    label_return_page2.configure(height=50)
    pathFace = filenameFace


def show_frame(frame):
    frame.tkraise()


def res():
    # Update các trường dữ liệu trên form
    res_imageFront = ImageTk.PhotoImage(
        Image.open(pathFront).resize((250, 200)))
    lb_res_front.configure(image=res_imageFront)
    lb_res_front.image = res_imageFront
    #
    res_imageBack = ImageTk.PhotoImage(Image.open(pathBack).resize((250, 200)))
    lb_res_back.configure(image=res_imageBack)
    lb_res_back.image = res_imageBack
    #
    res_imageFace = ImageTk.PhotoImage(Image.open(pathFace).resize((250, 200)))
    lb_res_face.configure(image=res_imageFace)
    lb_res_face.image = res_imageFace
    #
    num_face_input, num_face_selfie, face_distance = compare(
        pathFront, pathFace)
    print(num_face_input, num_face_selfie, face_distance)
    if (face_distance is not None):
        res_from_distance = face_distance < 0.55
        lb_res_facematch.configure(text='{}'.format(res_from_distance))
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
    else:
        messagebox.showerror(
            'Thông báo', 'Ảnh selfie hoặc ảnh CCCD không hợp lệ.')


# Create formFp
formF = Tk()
formF.title("Chương trình demo eKYC")
formF.geometry("900x700")
formF.rowconfigure(0, weight=1)
formF.columnconfigure(0, weight=1)
# formF.state('zoomed')
# setup page app
page1 = Frame(formF)
page2 = Frame(formF)
page3 = Frame(formF)
page4 = Frame(formF)
for frame in (page1, page2, page3, page4):
    frame.grid(row=0, column=0, sticky='nsew')
show_frame(page1)
### Image Icon ###
image_uploadFile = customtkinter.CTkImage(
    Image.open('./images/upload.png'), size=(30, 30))
image_continue = customtkinter.CTkImage(
    Image.open('./images/right-arrow.png'), size=(30, 30))
image_back = customtkinter.CTkImage(
    Image.open('./images/back.png'), size=(30, 30))
image_ocr = customtkinter.CTkImage(
    Image.open('./images/ocr1.png'), size=(30, 30))
image_facematch = customtkinter.CTkImage(Image.open(
    './images/face-recognition.png'), size=(30, 30))
photoF = PhotoImage(file="cmt.be3f6567.png")
photoB = PhotoImage(file="cmt_back.29611820.png")
imgFace = PhotoImage(file="face-id.png")
# ======== Page 1(Upload front photo) ========
lb_title_page1 = Label(page1,
                       text="Chụp lại ảnh Thẻ căn cước mặt trước của bạn",
                       font='Times 16 bold')
lb_title_page1.pack(side="top")
lb_notice_page1 = Label(
    page1,
    text="* Vui lòng sử dụng giấy tờ thật. Hãy đảm bảo ảnh chụp không bị mờ hoặc bóng, thông tin hiển thị rõ ràng, dễ đọc.",
    font='Times 8',
    fg='red')
lb_notice_page1.place(relx=0.5, rely=0.1, anchor=CENTER)
lb_photo_page1 = Label(page1, image=photoF)
lb_photo_page1.place(relx=0.5, rely=0.4, anchor=CENTER)
### Button page 1 ###
bt_uploadF = customtkinter.CTkButton(master=page1,
                                     text="Tải ảnh/ Chụp ảnh",
                                     image=image_uploadFile,
                                     text_color='white',
                                     font=customtkinter.CTkFont(
                                         family="Times", size=18, weight="bold"),
                                     width=600,
                                     height=50,
                                     corner_radius=10,
                                     fg_color='#2596be',
                                     hover_color="#336699",
                                     command=uploadF)
bt_uploadF.place(relx=0.5, rely=0.7, anchor=CENTER)
bt_continueF = customtkinter.CTkButton(master=page1,
                                       text="Tiếp theo",
                                       image=image_continue,
                                       text_color='white',
                                       font=customtkinter.CTkFont(
                                           family="Times", size=18, weight="bold"),
                                       corner_radius=10,
                                       fg_color='#2596be',
                                       hover_color="#336699",
                                       command=lambda: show_frame(page2))
# ======== Page 2(Upload back photo) ========
lb_title_page2 = Label(
    page2, text="Chụp lại ảnh Thẻ căn cước mặt sau của bạn", font='Times 16 bold')
lb_title_page2.pack(side="top")
lb_notice_page2 = Label(
    page2, text="* Vui lòng sử dụng giấy tờ thật. Hãy đảm bảo ảnh chụp không bị mờ hoặc bóng, thông tin hiển thị rõ ràng, dễ đọc.",
    font='Times 8', fg='red')
lb_notice_page2.place(relx=0.5, rely=0.1, anchor=CENTER)
lb_photo_page2 = Label(page2, image=photoB)
lb_photo_page2.place(relx=0.5, rely=0.4, anchor=CENTER)
### Button page 2 ###

bt_uploadB = customtkinter.CTkButton(master=page2,
                                     text="Tải ảnh/ Chụp ảnh",
                                     image=image_uploadFile,
                                     text_color='white',
                                     font=customtkinter.CTkFont(
                                         family="Times", size=18, weight="bold"),
                                     width=600,
                                     height=50,
                                     corner_radius=10,
                                     fg_color='#2596be',
                                     hover_color="#336699",
                                     command=uploadB)
bt_uploadB.place(relx=0.5, rely=0.7, anchor=CENTER)
bt_continueB = customtkinter.CTkButton(master=page2,
                                       text="OCR",
                                       image=image_ocr,
                                       text_color='white',
                                       font=customtkinter.CTkFont(
                                           family="Times", size=18, weight="bold"),
                                       corner_radius=10,
                                       fg_color='#2596be',
                                       hover_color="#336699",
                                       command=process)
label_return_page1 = customtkinter.CTkButton(master=page2,
                                             text="Quay lại",
                                             image=image_back,
                                             text_color='white',
                                             font=customtkinter.CTkFont(
                                                 family="Times", size=18, weight="bold"),
                                             corner_radius=10,
                                             fg_color='#2596be',
                                             hover_color="#336699",
                                             command=lambda: show_frame(page1))
# ======== Page 3(Upload Face photo) ========
lb_title_page3 = Label(
    page3, text="Chụp lại ảnh khuôn mặt của bạn", font='Times 16 bold')
lb_title_page3.pack(side="top")
label_photo_page3 = Label(page3, image=imgFace)
label_photo_page3.place(relx=0.5, rely=0.4, anchor=CENTER)
### Button page 3 ###
bt_uploadFace = customtkinter.CTkButton(master=page3,
                                        text="Tải ảnh/ Chụp ảnh",
                                        image=image_uploadFile,
                                        text_color='white',
                                        font=customtkinter.CTkFont(
                                            family="Times", size=18, weight="bold"),
                                        width=600,
                                        height=50,
                                        corner_radius=10,
                                        fg_color='#2596be',
                                        hover_color="#336699",
                                        command=uploadFace)
bt_uploadFace.place(relx=0.5, rely=0.75, anchor=CENTER,)
bt_continueFace = customtkinter.CTkButton(master=page3,
                                          text="Facematch",
                                          image=image_facematch,
                                          text_color='white',
                                          font=customtkinter.CTkFont(
                                              family="Times", size=18, weight="bold"),
                                          corner_radius=10,
                                          fg_color='#2596be',
                                          hover_color="#336699",
                                          command=res)
label_return_page2 = customtkinter.CTkButton(master=page3,
                                             text="Quay lại",
                                             image=image_back,
                                             text_color='white',
                                             font=customtkinter.CTkFont(
                                                 family="Times", size=18, weight="bold"),
                                             corner_radius=10,
                                             fg_color='#2596be',
                                             hover_color="#336699",
                                             command=lambda: show_frame(page2))
# ======== Page 4(Return result) ========
lb_title_page4 = Label(page4, text="Kết quả xác minh", font='Times 16 bold')
lb_title_page4.pack(side="top")
res_photo_front = ImageTk.PhotoImage(
    Image.open("cmt.be3f6567.png").resize((250, 200)))
lb_res_front = Label(page4, image=res_photo_front)
lb_res_front.place(relx=0.2, rely=0.2, anchor=CENTER)
res_photo_back = ImageTk.PhotoImage(Image.open(
    "cmt_back.29611820.png").resize((250, 200)))
lb_res_back = Label(page4, image=res_photo_back)
lb_res_back.place(relx=0.5, rely=0.2, anchor=CENTER)
res_photo_face = ImageTk.PhotoImage(
    Image.open("face.c8f1db03.png").resize((250, 200)))
lb_res_face = Label(page4, image=res_photo_face)
lb_res_face.place(relx=0.8, rely=0.2, anchor=CENTER)
#
lb_show_facematch = Label(page4, text="Face match : ", font='Time 12 bold')
lb_show_facematch.place(relx=0.1, rely=0.38, anchor="w")
lb_res_facematch = Label(page4, text="N/A", font='Time 14 bold', fg='green')
lb_res_facematch.place(relx=0.4, rely=0.38, anchor="w")
#
lb_show_id = Label(page4, text="Số CCCD : ", font='Time 12 bold')
lb_show_id.place(relx=0.1, rely=0.43, anchor="w")
lb_res_id = Label(page4, text="N/A", font='Time 12')
lb_res_id.place(relx=0.4, rely=0.43, anchor="w")
#
lb_show_name = Label(page4, text="Họ và tên : ", font='Time 12 bold')
lb_show_name.place(relx=0.1, rely=0.48, anchor="w")
lb_res_name = Label(page4, text="N/A", font='Time 12')
lb_res_name.place(relx=0.4, rely=0.48, anchor="w")
#
lb_show_dob = Label(page4, text="Ngày sinh : ", font='Time 12 bold')
lb_show_dob.place(relx=0.1, rely=0.53, anchor="w")
lb_res_dob = Label(page4, text="N/A", font='Time 12')
lb_res_dob.place(relx=0.4, rely=0.53, anchor="w")
#
lb_show_sex = Label(page4, text="Giới tính : ", font='Time 12 bold')
lb_show_sex.place(relx=0.1, rely=0.58, anchor="w")
lb_res_sex = Label(page4, text="N/A", font='Time 12')
lb_res_sex.place(relx=0.4, rely=0.58, anchor="w")
#
lb_show_nationality = Label(page4, text="Quốc tịch : ", font='Time 12 bold')
lb_show_nationality.place(relx=0.1, rely=0.63, anchor="w")
lb_res_nationality = Label(page4, text="N/A", font='Time 12')
lb_res_nationality.place(relx=0.4, rely=0.63, anchor="w")
#
lb_show_address = Label(page4, text="Quê quán : ", font='Time 12 bold')
lb_show_address.place(relx=0.1, rely=0.68, anchor="w")
lb_res_address = Label(page4, text="N/A", font='Time 12')
lb_res_address.place(relx=0.4, rely=0.68, anchor="w")
#
lb_show_home = Label(page4, text="Nơi thường trú : ", font='Time 12 bold')
lb_show_home.place(relx=0.1, rely=0.73, anchor="w")
lb_res_home = Label(page4, text="N/A", font='Time 12')
lb_res_home.place(relx=0.4, rely=0.73, anchor="w")
#
lb_show_doe = Label(page4, text="Ngày hết hạn : ", font='Time 12 bold')
lb_show_doe.place(relx=0.1, rely=0.78, anchor="w")
lb_res_doe = Label(page4, text="N/A", font='Time 12')
lb_res_doe.place(relx=0.4, rely=0.78, anchor="w")
#
lb_show_features = Label(
    page4, text="Đặc điểm nhận dạng : ", font='Time 12 bold')
lb_show_features.place(relx=0.1, rely=0.83, anchor="w")
lb_res_features = Label(page4, text="N/A", font='Time 12')
lb_res_features.place(relx=0.4, rely=0.83, anchor="w")
#
lb_show_issue_date = Label(page4, text="Ngày cấp : ", font='Time 12 bold')
lb_show_issue_date.place(relx=0.1, rely=0.88, anchor="w")
lb_res_issue_date = Label(page4, text="N/A", font='Time 12')
lb_res_issue_date.place(relx=0.4, rely=0.88, anchor="w")
#
label_return_page3 = customtkinter.CTkButton(master=page4,
                                             text="Quay lại",
                                             image=image_back,
                                             text_color='white',
                                             font=customtkinter.CTkFont(
                                                 family="Times", size=18, weight="bold"),
                                             corner_radius=10,
                                             height=50,
                                             fg_color='#2596be',
                                             hover_color="#336699",
                                             command=lambda: show_frame(page3))
label_return_page3.place(relx=0.5, rely=0.95, anchor=CENTER)
formF.mainloop()
