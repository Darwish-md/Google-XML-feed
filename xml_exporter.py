import xml.etree.ElementTree as xml

def generate_xml(file, rows):

    root = xml.Element("products")
    # to be used as a flag for the if condition determining if the current record has the same product as previous one
    previous_id = None
    '''
    As from the query, we will have number of rows and in each row we will have: 
        row[0] => product_id
        row[1] => title
        row[2] => description
        row[3] => ean or gtin
        row[4] => quantity 
        row[5] => price
        row[6] => image
        row[7] => additional_image_link
        row[8] => brand
    '''
    for row in rows:
        ''' to check if the same product has more than record (due to having more than one additional_image_link)
            if so, just the additional_image_link is appended to the product specified by the id and skip the rest of the for loop to check next record
        '''
        if (row[0] == previous_id):
            str = ".//product[@id='{}']".format(row[0])
            product = root.find(str)
            additional_image_link = xml.SubElement(product, "additional_image_link")
            additional_image_link.text = "https://butopea.com/{}".format(row[7])
            continue

        #creating the sub-elements of the product node
        product = construct_node(row)
        
        root.append(product)

        #update the vlaue to be equal to the new product_id
        previous_id = row[0]

        tree = xml.ElementTree(root)

        #open the file in write binary mode and saving the details in utf8 format
        with open(file, "wb") as files:
            tree.write(files, encoding='utf8')

def construct_node(row):
        #product_id
        product = xml.Element("product")
        #to set the id attribute to be able to reference the product in the if statement
        product.set('id', row[0])
        id = xml.SubElement(product, "id")
        id.text = row[0]

        #title
        title = xml.SubElement(product, "title")
        title.text = row[1]

        #description
        description = xml.SubElement(product, "description")
        description.text = row[2]

        #ean
        gtin = xml.SubElement(product, "gtin")
        gtin.text = row[3]

        # if the quantity is greater than zero then we return "in_stock", else we return "out_of_stock"
        availability = xml.SubElement(product, "availability")
        if(row[4] > 0):
            availability.text = "in_stock"
        else: availability.text = "out_of_stock"

        #price
        price = xml.SubElement(product, "price")
        price.text = "{} HUF".format(row[5])

        #brand
        brand = xml.SubElement(product, "brand")
        brand.text = row[8]

        #condition which is always new for all products
        condition = xml.SubElement(product, "condition")
        condition.text = "new"

        #link to the product page
        link = xml.SubElement(product, "link")
        link.text = "https://butopea.com/p/" + row[0]

        #image_link
        image_link = xml.SubElement(product, "image_link")
        image_link.text = "https://butopea.com/" + row[6]

        #additional_image_link
        additional_image_link = xml.SubElement(product, "additional_image_link")
        additional_image_link.text = "https://butopea.com/" + row[7]

        return product
        