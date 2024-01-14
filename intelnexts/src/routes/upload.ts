import express from 'express';
const auth = require("../controllers/auth")

const controller = require('../controllers/upload')

const router = express.Router()

// bajo el path /upload se crea el metodo post el cual recibe un form-data, el nombre de la variable debe ser """file"""
// es necesario que en header se incluya la authentification con bearer y el token generado en /auth/createToken

router.post(
    `/`,  auth.authenticateToken,
    controller.upload,
    controller.uploadFile
)

module.exports = router