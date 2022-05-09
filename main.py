import os
import sys
import glob
import cv2
import img2pdf
from PyPDF2 import PdfFileWriter, PdfFileReader

# 引数（画像ファイルがあるフォルダ）を取得する
args = sys.argv
folderPath = args[1]

# ファイルリストを取得する
images = glob.glob(os.path.join(folderPath, "*"))
print(images)
# しおりのデータ
bookmarks = []

# QRコードを認識する
for i in range(len(images)):
    # 画像ファイルリストを表示する
    print(images[i])
    # 画像ファイルを開く
    image = cv2.imread(images[i])
    # QRコードを認識する
    qrDetector = cv2.QRCodeDetector()
    data, bbox, rectifiedImage = qrDetector.detectAndDecode(image)
    # 画像をプレビュー
    # cv2.imshow("Rectified QRCode", images[i])
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    print(data)
    # しおりデータを追加
    if data!="":
        bookmarks.append([i, data])

# 画像をPDFファイルに変換する
with open(os.path.basename(folderPath)+".org.pdf", "wb") as f:
    f.write(img2pdf.convert(images))

if len(bookmarks)>0:
    # PyPDF2でPDFファイルを開く
    input = PdfFileReader(os.path.basename(folderPath)+".org.pdf")

    # PdfFileWriterのインスタンスを作成
    output = PdfFileWriter()

    # オリジナルのPDFをPdfFileWriterにコピーする
    output.cloneDocumentFromReader(input)

    # しおりを追加する
    for i in range(len(bookmarks)):
        print("addBookmark "+str(bookmarks[i][0]))
        output.addBookmark(bookmarks[i][1], bookmarks[i][0])

    # PDFを出力する
    with open(os.path.basename(folderPath)+".pdf", 'wb') as o:
        output.write(o)
else:
    os.rename(os.path.basename(folderPath)+".org.pdf",os.path.basename(folderPath)+".pdf")
