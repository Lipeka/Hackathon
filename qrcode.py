import segno

# Replace 'YOUR_SHAREABLE_LINK' with the actual shareable link to your PowerPoint presentation
shareable_link = 'https://docs.google.com/presentation/d/1yG92uHeDDI-RpWefFjgvw9riAf1xvxMgCFnaTt6y5wQ/edit?usp=drive_link'
qrcode = segno.make_qr(shareable_link)

qrcode.save(
    "lightblue_qrcode.png",
    scale=5,
    light="lightblue",
)

qrcode.show()
