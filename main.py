import streamlit as st
from yeni_kisiler import elemanlar, ekip_cesit
import fitz  
from datetime import datetime, time, timedelta

now = datetime.now()
formatted_date = now.strftime("%d/%m/%Y")
clock = now.time()
check_clock = time(hour = 19)
next_day = now + timedelta(days=1)
formatted_next_day = next_day.strftime('%d/%m/%Y')

normal = False
gunduz = True

if clock > check_clock:
    gunduz = False

SIFRE = 'htkmfic'

if "dogrulandi" not in st.session_state:
    st.session_state.dogrulandi = False

if not st.session_state.dogrulandi:
    sifre = st.text_input("Lütfen şifreyi girin:", type="password")

    if sifre == SIFRE:
        st.session_state.dogrulandi = True
        st.success("Şifre doğru! İçeriği yüklemek için buraya tıklayın.")
    elif sifre:
        st.error("Yanlış şifre! Tekrar deneyin.")
else:
    col1, col2, col3 = st.columns(3)

    with col1:
        ofis = st.radio('Ofis', options=['FIC', 'NOTAM', 'AFTN'])
        
    
    with col2:
        ekip = st.radio('Ekip', options=ekip_cesit)
        st.write('<div style="height:20px;"></div>', unsafe_allow_html=True) 


    elemanlarr = sorted([item for item in elemanlar if item['ofis'] == ofis and item['ekip'] == ekip], key=lambda x: x['numara'])
    gunasiricilar = [item for item in elemanlar if item['ofis'] == ofis and item['gorev'] == 'gunasiri' and (ekip in item['ekipler'])]
    eksikler = []
    sebepler = []

    if gunduz:
        tam_elemanlar = elemanlarr[:] + gunasiricilar
        mevcut_elemanlar = elemanlarr[:] + gunasiricilar
        start_time = f'{formatted_date} - 05:30 UTC'
        end_time = f'{formatted_date} - 17:00 UTC'
        start_hour = '05:30 UTC'
        end_hour = '17:00 UTC'

        with col3:
            vardiya = st.radio('Normalciler', options=['Var', 'Yok'])
        
        if vardiya == 'Var':
            normal = True
            tam_normalciler = sorted([item for item in elemanlar if item['gorev'] == 'normal' and item['ofis'] == ofis], key=lambda x: x['numara'])
            mevcut_normalciler = sorted([item for item in elemanlar if item['gorev'] == 'normal' and item['ofis'] == ofis], key=lambda x: x['numara'])
    else:
        tam_elemanlar = elemanlarr[:]
        mevcut_elemanlar = elemanlarr[:]
        start_time = f'{formatted_date} - 16:30 UTC'
        end_time = f'{formatted_next_day} - 06:00 UTC'
        start_hour = '16:30 UTC'
        end_hour = '06:00 UTC'

        with col3:
            st.write('<div style="height:100px;"></div>', unsafe_allow_html=True) 

    with col1:
        st.write('')
        st.write('')
        st.write('<div style="height:30px;"></div>', unsafe_allow_html=True) 

    with col1:
        st.write("Ekipten kimler eksik?")
        for eleman in tam_elemanlar:
            if st.checkbox(eleman['isim'], key=f'{eleman['init']}_{eleman['isim']}'):
                eksikler.append(eleman)
                mevcut_elemanlar.remove(eleman)
            

    if eksikler:
            with col3:
                st.write('')
                st.write('<div style="height:70px;"></div>', unsafe_allow_html=True) 
                for eleman in eksikler:
                    sebep = st.selectbox(f"{eleman['isim']} gelmeme sebebi:", 
                                    ["SENELİK İZİNLİ", 
                                        "MAZERET İZİNLİ", 
                                        "RAPORLU",
                                        "HARİÇTE GÖREVLİ",
                                        'HASTANEDE',
                                        'İDARİ İZİNLİ',
                                        'NÖBET İZİNLİ'], key=f"{eleman['init']}_{eleman['isim']}_sebep")
                    sebepler.append(sebep)


    with col2:
        st.write('')
        

    if normal:
        with col2:
            st.write("Normalcilerden kimler eksik?")
            for normalci in tam_normalciler:
                if st.checkbox(normalci['isim'], key=f'{normalci['init']}_{normalci['isim']}'):
                    #eksikler.append(eleman)
                    mevcut_normalciler.remove(normalci)


    pdf_path = "source/vukuat.pdf"
    pdf_document = fitz.open(pdf_path)

    font_path = 'source/CALIBRI.TTF'
    font_path_bold = 'source/CALIBRIB.TTF'

    page = pdf_document[0]

    delx1, delx2 = 180, 310
    dely1, dely2 = 100, 115
    page.draw_rect((delx1, dely1, delx2, dely2), color=(1, 1, 1), fill=(1, 1, 1))

    delx11, delx22 = 450, 580
    dely11, dely22 = 100, 115
    page.draw_rect((delx11, dely11, delx22, dely22), color=(1, 1, 1), fill=(1, 1, 1))



    htkm = 'HTKM'
    x_htkm = 255
    y_htkm = 90  
    page.insert_text((x_htkm, y_htkm), htkm, fontsize=14, fontname="Calibrib", fontfile = font_path_bold,color=(0, 0, 0))


    aim_ofis = f'AIM/{ofis}'
    if ofis == 'FIC':
        x_fic = 433
    elif ofis == 'NOTAM':
        x_fic = 424
    else:
        x_fic = 428
    
    y_fic = 90  
    page.insert_text((x_fic, y_fic), aim_ofis, fontsize=12, fontname="Calibrib", fontfile = font_path_bold, color=(0, 0, 0))


    x_ekip = 533
    y_ekip = 90  
    page.insert_text((x_ekip, y_ekip), ekip, fontsize=14, fontname="Calibrib", fontfile = font_path_bold, color=(0, 0, 0))

    x1 = 185
    y1 = 115  
    page.insert_text((x1, y1), start_time, fontsize=12, fontname="Calibrib", fontfile = font_path_bold, color=(0, 0, 0))


    x1 = 455
    y1 = 115  
    page.insert_text((x1, y1), end_time, fontsize=12, fontname="Calibrib", fontfile = font_path_bold, color=(0, 0, 0))


    eleman_counter = 0
    for eleman in mevcut_elemanlar:
        name = eleman['isim']
        init = eleman['init']
        hours = f'{start_hour[:-4]}    {end_hour[:-4]}'
        x = 116
        x_init = x + 121
        x_hour = x - 68
        y = 170 + 43*eleman_counter
        name_font = 12
        if eleman['uzunisim'] == True:
            name_font = 10
        page.insert_text((x, y), name, fontsize=name_font, fontname="Calibri", fontfile = font_path,color=(0, 0, 0))
        page.insert_text((x_init, y), init, fontsize=12, fontname="Calibri", fontfile = font_path,color=(0, 0, 0))
        page.insert_text((x_hour, y), hours, fontsize=11, fontname="Calibri", fontfile = font_path,color=(0, 0, 0))
        

        eleman_counter += 1

    if normal:
        normal_counter = 0
        for normalci in mevcut_normalciler:
            name = normalci['isim']
            init = normalci['init']
            hours = f'05:30    14:00'
            x = 385
            x_init = x + 113
            x_hour = x - 68
            y = 170 + 43*normal_counter
            name_font = 12
            if normalci['uzunisim'] == True:
                name_font = 10
            page.insert_text((x, y), name, fontsize=name_font, fontname="Calibri", fontfile = font_path,color=(0, 0, 0))
            page.insert_text((x_init, y), init, fontsize=12, fontname="Calibri", fontfile = font_path,color=(0, 0, 0))
            page.insert_text((x_hour, y), hours, fontsize=11, fontname="Calibri", fontfile = font_path,color=(0, 0, 0))

            normal_counter += 1


    for i, eksik in enumerate(eksikler):
        name = eksik['isim']
        sebep = sebepler[i]
        mazeret = f'{name} ({sebep})'
        x = 48
        y = 598 + 14.3*i
        page.insert_text((x, y), mazeret, fontsize=12, fontname="Calibri", fontfile = font_path,color=(0, 0, 0))

    page2 = pdf_document[1]
    ekip_sefi = mevcut_elemanlar[0]['isim']
    x = 25
    y = 727
    page2.insert_text((x, y), ekip_sefi, fontsize=14, fontname="Calibri", fontfile = font_path,color=(0, 0, 0))

    output_pdf_path = "guncellenmis_vukuat.pdf"
    pdf_document.save(output_pdf_path)
    pdf_document.close()


    with open(output_pdf_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
        with col2:
            st.write('<div style="height:150px;"></div>', unsafe_allow_html=True) 
            if not gunduz or not normal:
                st.write('<div style="height:162px;"></div>', unsafe_allow_html=True) 
            st.download_button(
                label="Vukuat Formunu İndir",
                data=pdf_bytes,
                file_name=f"{ekip}_Ekibi_{formatted_date}_Vukuat.pdf",
                mime="application/pdf"
            )

