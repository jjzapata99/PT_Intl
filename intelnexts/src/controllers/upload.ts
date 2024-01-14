import {signPDF} from "./signer";


const multer = require('multer')

const storage = multer.diskStorage({
    destination: function (req: any, file: any, cb: any) {
        cb(null, 'uploads')
    },
    filename: function (req:any, file:any, cb:any) {
        cb(null, `toSigned.${file.originalname.split('.')[1]}`)
    }
})

const upload = multer({ storage: storage })

// Recibe y guarda el archivo pdf, cabe recalcar que el nombre debe coincidir con el parametro que se envio junto al archivo
// en el metodo post

exports.upload = upload.single('file')

// devuelve un objeto el cual hace referencia al firmado exitoso

exports.uploadFile = (req:any, res:any) => {
    signPDF()
    res.send({ "response": 'Se ha recibido y firmado el archivo' })
}