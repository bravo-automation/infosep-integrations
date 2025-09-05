import requests, json
from datetime import datetime
from helpers.products import TecnoGlobalProduct
from helpers.excel_generator import CustomExcelGenerator

class TecnoGlobal():
    def __init__(self):
        config = {}
        with open('config.properties', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()

        self.url = config['tg_url']
        auth = config['tg_auth']
        self.payload = ""
        self.headers = {
            "Authorization": f"Basic {auth}"
        }
        self.all_product_file = 'products/tecnoglobal.json'

    def generate_excel_news(self):
        with open('products/all_products.json', encoding='utf-8', mode='r') as currentFile:
            data=currentFile.read().replace('\n', '')
            products = json.loads(data)
    
        tg_new = []
        total = 0
        for prod in products["products"]:
            if prod['infosep']['infosep_id'] == 0:
                total += 1
                del prod['tg']['desc']
                del prod['tg']['images']
                prod['tg']['category'] = prod['tg']['cat'][0]
                prod['tg']['subCategory'] = prod['tg']['cat'][1]
                del prod['tg']['cat']
                tg_new.append(prod['tg'])

        excel = CustomExcelGenerator(tg_new, generic_excel=True, auto_filter=True)
        excel.dict_to_excel()

        #print(total)

    def generate_excel(self):
        now = datetime.now()    
        dt_string = now.strftime("%Y%m%d_%H%M%S")
        tg_output_excel_file = 'tb_product_control_'+dt_string+'.xlsx'

        for item in self.tg_data:
            item.pop('upcEan13', None)
            item.pop('ofertaSiNo', None)
            item.pop('tipoMoneda', None)
            item.pop('timeStamp', None)
            item.pop('subSubCategoria', None)
            item.pop('imagenes', None)
            item.pop('descripcionExtendida', None)
            item.pop('pdf', None)
            item.pop('scripts', None)
            item.pop('videos', None)
            item.pop('atributos', None)
            item.pop('packaging', None)

        excel = CustomExcelGenerator(self.tg_data)
        excel.output_file=tg_output_excel_file
        excel.column_mapping = {
            "pnFabricante": "PN",
            "descripcion": "NAME",
            "precio": "TG_PRICE",
            "categoria": "CAT",
            "subCategoria": "SUBCAT",
            "marca": "BRAND",
            "stockDisp": "STOCK",
            "dolarTg": "DOLAR",
            "codigoTg": "TG_CODE"
        }
        excel.desired_order = [
            "PN", "TG_CODE", "NAME", "CAT", "SUBCAT", "DOLAR", "TG_PRICE", "BRAND", "STOCK"
        ] 
        excel.auto_adjust = ['PN', 'TG_CODE', 'NAME', 'TG_PRICE']
        excel.auto_filter = True
        excel.dict_to_excel()

    def get_products_organized_file(self):
        with open(self.all_product_file, encoding='utf-8', mode='r') as currentFile:
            data=currentFile.read().replace('\n', '')
        return json.loads(data)

    def get_products_file(self, tg_filename):
        self.tg_filename = tg_filename
        with open(self.tg_filename, encoding='utf-8', mode='r') as currentFile:
            data=currentFile.read().replace('\n', '')
            tg_data = json.loads(data)
        self.tg_data = tg_data["products"]

    def organize_product_name(self, pn, brand, subCat, name):
        if brand == "AMD":
            if "Procesador" in name:
                name = name.replace("Procesador es AMD", "Procesador AMD")
                name = name.replace("Procesador  AMD", "Procesador AMD")
                name = name.replace("Procesador RYZEN", "Procesador AMD Rayzen")
                name = name.replace("RYZEN", "Ryzen")

        if brand == "AOC":
            p_name = name.split()
            for word in p_name:
                if len(word) > 3:
                    if word in pn:
                        pn = word
                        break
            name = name.replace(f'{pn} ', "")
            if not "Monitor AOC" in name:
                name = name.replace("Monitor ", "Monitor AOC ")
                name = name.replace("MONITOR ", "Monitor AOC ")
            if not "Televisor AOC Roku TV" in name:
                if "Roku TV" in name:
                    name = name.replace("AOC Roku TV", "Televisor AOC Roku TV")
            name = name+" "+pn
            pass

        if "AMERICAN POWER" in brand:
            pn_end = False
            p_name = name.split()
            for word in p_name:
                if len(word) > 3:
                    if word in pn:
                        pn = word
                        pn_end = True
                        break
            if pn_end:
                name = name.replace(f'{pn} ', "")
                name = name+" "+pn

        if "BROTHER" in brand:
            pn_end = False
            p_name = name.split()
            for word in p_name:
                if len(word) > 3:
                    if word in pn:
                        pn = word
                        pn_end = True
                        break
            if pn_end:
                name = name.replace(f'{pn} ', "")
                name = name+" "+pn
            
            if subCat == "Accesorios":
                name = name.replace("Cinta ", "Cinta Brother ")
            suministros = ['Suministros Laser','Suministros Tinta']
            if subCat in suministros:
                name = name.replace("TONER BROTHER ", "Toner Brother ")
                name = name.replace("Toner BROTHER ", "Toner Brother ")
                name = name.replace("NEGRO", "Negro")
                name = name.replace("negra", "Negra")
                name = name.replace("YELLOW", "Yellow")
                name = name.replace("AZUL PASTEL ", "Azul Pastel ")
                name = name.replace("AZUL", "Azul")
                name = name.replace("AMARILLO", "Amarillo")
                name = name.replace("amarilla", "Amarilla")
                name = name.replace("MAGENTA", "Magenta")
                name = name.replace("magenta", "Magenta")
                name = name.replace("ROJO", "Rojo")
                name = name.replace("CYAN", "Cyan")
                name = name.replace("CARTRIDGE BROTHER", "Catridge Brother")
                name = name.replace("BOTELLA ", "Botella ")
                name = name.replace("DRUM BROTHER ", "Drum Brother ")
                name = name.replace("Drum BROTHER ", "Drum Brother ")

        if "ASUS" in brand:
            if subCat == "Placas madre":
                name = name.replace("Placa ", "Tarjeta ")
                name = name.replace("Tarjeta madre ", "Tarjeta Madre ")
                name = name.replace(" PRIME ", " Prime ")
                name = name.replace(" Prime Prime ", " Prime ")
                name = name.replace("Tarjeta Madres ", "Tarjeta Madre Asus")
                name = name.replace("Tarjeta Madre Prime", "Tarjeta Madre Asus Prime")
                name = name.replace("AsusASUS", "Asus")
                name = name.replace("Tarjeta Madre Asus/", "Tarjeta Madre Asus /")
            if subCat == "Computador desktop":
                name = name.replace("DESKTOP ASUS ", "Desktop AIO ASUS ")
            if subCat == "Computador Notebook":
                name = name.replace("NOTEBOOK ASUS ", "Notebook ASUS ")

        if "DELL" in brand:
            if subCat == "Computador Notebook":
                name = name.replace("Notebook NBK Latitude ", "Notebook Dell Latitude ")
                name = name.replace("Notebook Latitude ", "Notebook Dell Latitude ")
                name = name.replace("NBK Latitude ", "Notebook Dell Latitude ")
                name = name.replace("NBK XPS ", "Notebook Dell XPS ")
                name = name.replace("WS NBK Precision ", "Notebook WS Dell Precision ")
                name = name.replace("Notebook DELL Latitude ", "Notebook Dell Latitude ")

        if "HP" in brand:
            if subCat == "Computador Notebook":
                name = name.replace("Notebook NB ", "Notebook HP ")
                name = name.replace("HP NB ", "Notebook HP ")
                name = name.replace("NB ", "Notebook HP ")
            if subCat == "Computador desktop":
                name = name.replace("Computador AIO ", "Computador HP AIO ")
                if not "Computador HP AIO" in name:
                    name = "Computador HP AIO "+name

        if brand == "KENSINGTON":
            name = name.replace("Adaptador USB-C a Ethernet ", "Adaptador Kensington USB-C a Ethernet")
            name = name.replace("Apoya Munecas ", "Apoya Muñecas Kensington ")
            name = name.replace("APOYA MUNECAS ", "Apoya Muñecas Kensington ")
            name = name.replace("Apoya Pies ", "Apoya Pies Kensington ")
            if "Audifono" in name:
                name = name.replace("Audifono Audifono ", "Audífono Kensington ")
                name = name.replace("Audifono Audifonos ", "Audífono Kensington ")
            name = name.replace("Base para monitor ", "Base para Monitor Kensington ")
            name = name.replace("Base para Notebook ", "Base para Notebook Kensington ")
            name = name.replace("Base para Ntbk ", "Base para Notebook Kensington ")
            name = name.replace("Brazo para Monitor ", "Brazo para Monitor Kensington ")
            name = name.replace("Cable de Seguridad ", "Cable de Seguridad Kensington ")
            name = name.replace("Mochila ", "Mochila Kensington ")
            if "Mouse" in name:
                if "Mouse Pad" in name:
                    name = name.replace("Mouse Pad ", "Mouse Pad Kensington ")
                    name = name.replace("MOUSE PAD ", "Mouse Pad Kensington ")
                else:
                    name = name.replace("Mouse ", "Mouse Kensington ")
                    name = name.replace("MOUSE ", "Mouse Kensington ")
            name = name.replace("Teclado ", "Teclado Kensington ")
            name = name.replace("Trituradora ", "Trituradora Kensington ")

        if "KINGSTON" in brand:
            if "Disco Duro" in subCat:
                name = name.replace("Disco Duro ", "Disco Duro Kingston ")
            if subCat == "Memoria Flash":
                if "Memoria" in name:
                    name = name.replace("Memoria ", "Memoria Flash Kingston ")
                else:
                    name = "Memoria Flash Kingston "+ name
            if subCat == "Memorias RAM":
                if "Memoria" in name:
                    name = name.replace("Memoria ", "Memoria RAM Kingston ")
                else:
                    name = "Memoria Flash Kingston "+ name
            if subCat == "Pendrive":
                if "Pendrive" in name:
                    name = name.replace("Pendrive ", "Pendrive Kingston ")
                else:
                    name = "Pendrive Kingston "+ name

        if "LENOVO" in brand:
            name = name.replace("THINKPAD ", "ThinkPad ")
            name = name.replace("NB ", "Notebook Lenovo ")	

            if brand == "LENOVO ACCESORIOS":
                name = name.replace("Adaptador USB-C a HDMI ", "Adaptador Lenovo USB-C a HDMI")


        if brand == "LG ELECTRONICS":
            if not "Monitor LG " in name:
                name = name.replace("Monitor Gaming ", "Monitor LG Gaming ")
                name = name.replace("Smart Monitor 27 ", "Monitor LG Smart 27 ")
                name = name.replace("Monitor 27 ", "Monitor LG 27 ")
                name = name.replace("Monitor 34 ", "Monitor LG 34 ")
                if "MONITOR LG" in name:
                    name = name.replace("MONITOR LG ", "")
                    name = "Monitor LG "+name
                if "Monitor with" in name:
                    name = "Monitor LG "+name

        if brand == "SEAGATE":
            name = name.replace("Duisco Duro ", "")
            name = name.replace(" Interno", "")
            name = name.replace("Seagate ", "")
            name = name.replace("Disco Duro ", "Disco Duro Seagate ")
            pass

        if brand == "PHILLIPS":
            pn_end = False
            p_name = name.split()
            for word in p_name:
                if len(word) > 3:
                    if word in pn:
                        pn = word
                        pn_end = True
                        break
            if pn_end:
                if subCat == "Televisores":
                    name = name.replace(pn, "Televisor")
                if subCat == "Tv / Monitor":
                    name = name.replace(pn, "Monitor")
                if subCat == "Accesorios computacion":
                    name = name.replace(pn+' ', "")
                    name = name+" "+pn

        if brand == "PNY":
            name = name.replace("Tarjeta de Video PNY /NVIDIA", "Tarjeta de Video PNY NVIDIA")
            name = name.replace("Tarjeta de Video NVIDIA", "Tarjeta de Video PNY NVIDIA")

        if "SAMSUNG" in brand:
            if brand == "SAMSUNG MONITORES Y TV":
                name = name.replace("Monitor ", "Monitor Samsung ")
                name = name.replace("MON ", "Monitor Samsung ")
                name = name.replace("Pantalla ", "Pantalla Samsung ")
                name = name.replace("Mon Samsung ", "") 
                name = name.replace("Mon Prof Samsung ", "")

                pn_end = False
                p_name = name.split()
                for word in p_name:
                    if len(word) > 3:
                        if word in pn:
                            pn = word
                            pn_end = True
                            break
                if pn_end:
                    name = name.replace(f' {pn} ', " ")
                    name = name+" "+pn
            
            if brand == "SAMSUNG - M. PROFESIONALES":
                if not "Pantalla Samsung" in name:
                    name = name.replace("Pantalla ", "Pantalla Samsung ")
                name = name.replace("Mon ", "")
                name = name.replace("Crystal ", "Monitor Samsung Crystal ")

                pn_end = False
                p_name = name.split()
                for word in p_name:
                    if len(word) > 3:
                        if word in pn:
                            pn = word
                            pn_end = True
                            break
                if pn_end:
                    name = name.replace(f'{pn} ', "")
                    name = name+" "+pn

            if brand == "SAMSUNG NOTEBOOKS Y TABLET":
                if subCat == "Tablets":
                    pn_end = False
                    p_name = name.split()
                    for word in p_name:
                        if len(word) > 3:
                            if word in pn:
                                pn = word
                                pn_end = True
                                break
                    if pn_end:
                        name = name.replace(f' {pn} ', " ")
                        name = name+" "+pn

                    if "Tablet Samsung Galaxy" in name:
                        name = name.replace("Tablet Samsung Galaxy Tab", "Tablet Samsung Galaxy")
                    name = name.replace("Tablet GALAXY TAB ", "Tablet Galaxy Tab ")
                    name = name.replace("Tablet Galaxy Tab ", "Tablet Samsung Galaxy ")
                    name = name.replace("Galaxy Tab ", "Tablet Samsung Galaxy ")
                    name = name.replace("Tablet Tab ", "Tablet Samsung Galaxy ")
                    pass
        '''
        if "SAMSUNG" in brand:
            if "Monitor" in name:
                p_name = name.split()
                for word in p_name:

                    if len(word) > 3:
                        if word in pn:
                            pn = word
                            pn_end = True
                            break
                #if pn =='LH43QM':
                pn_end = False
                name = name.replace("Monitor ", "Monitor Samsung ")
                name = name.replace("SamsungSamsung", "Samsung")
                name = name.replace("Samsung Samsung", "Samsung")
                name = name.replace("MON ", "Mon ")
                name = name.replace("Mon Samsung", "Monitor Samsung")
                name = name.replace("Samsung Prof", "Prof")

                if str(name).count("Monitor Samsung") == 2:
                    last_mon = name.rfind("Monitor Samsung")
                    name = name[:last_mon] + name[last_mon + len("Monitor Samsung "):]

                if str(name).count("Samsung") == 2:
                    last_mon = name.rfind("Samsung")
                    name = name[:last_mon] + name[last_mon + len("Samsung "):]

                if pn_end:
                    name = name.replace(pn, "X")
                    name = name+' '+pn
                    name = name.replace(" X ", " ")
                pass
            '''
            
        return name

    def organize_products(self):
        all_products = []
        arr_names = []
        for prod in self.tg_data:
            try:
                imagenes = prod["imagenes"]
            except:
                imagenes = None

            try:
                descripcion = prod["descripcionExtendida"]
            except:
                descripcion = "Sin descripción"
            name = self.organize_product_name(prod['pnFabricante'], prod['marca'], prod["subCategoria"], prod["descripcion"])
            #if "LENOVO" in prod['marca']:
            if "LENOVO ACCESORIOS" == prod['marca']:
                arr_names.append(name)
            tg_prod = TecnoGlobalProduct(prod["pnFabricante"], name, descripcion, [prod["categoria"], prod["subCategoria"]], prod["precio"], prod["marca"], prod["stockDisp"], imagenes, prod["codigoTg"])
            all_products.append(tg_prod.get_product())

        with open(self.all_product_file, 'w') as f:
            json.dump(all_products, f)
        f.close()

        with open('names.json', 'w') as f:
            json.dump(arr_names, f)
        f.close()

        return self.all_product_file

    def save_all_product_file(self, inf_filename, tg_filename):
        with open(inf_filename, encoding='utf-8', mode='r') as currentFile:
            data=currentFile.read().replace('\n', '')
            inf_data = json.loads(data)
        
        with open(tg_filename, encoding='utf-8', mode='r') as currentFile:
            data=currentFile.read().replace('\n', '')
            tg_data = json.loads(data)

        #SAVE tg_dolar
        tg_data_tmp = tg_data["products"]
        for prod in inf_data["products"]:
            response = self.find_product(prod["infosep"]["id"], tg_data_tmp)
            if response:
                tg_prod = TecnoGlobalProduct(response["pnFabricante"], response["descripcion"], [response["categoria"], response["subCategoria"]], response["precio"], response["marca"], response["stockDisp"], response["imagenes"], response["codigoTg"])
                #CONTINUAR DAQUI

    def find_product(self, prod_pn):
        for prod in self.tg_data:
            if prod_pn == prod["pnFabricante"]:
                print(f'{prod["pnFabricante"]} product found')
                try:
                    imagenes = prod["imagenes"]
                except:
                    imagenes = None
                tg_prod_found = TecnoGlobalProduct(prod["pnFabricante"], prod["descripcion"], [prod["categoria"], prod["subCategoria"]], prod["precio"], prod["marca"], prod["stockDisp"], imagenes, prod["codigoTg"])
                return tg_prod_found
        return None

    def get_products(self):
        #TODO handle with error on the request
        print("Downloading products from TecngoGlobal API")
        response = requests.request("GET", self.url, data=self.payload, headers=self.headers)
        return self.save_product_file(response)

    def save_product_file(self, response):
        now = datetime.now()    
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%Y%m%d_%H%M%S")
        file_name = 'tecnoglobal_'+dt_string+'.json'
        with open(file_name, 'w') as f:
            json.dump(response.json(), f)
        f.close()
        print("Saving "+file_name)

        self.get_products_file(file_name)
        return file_name