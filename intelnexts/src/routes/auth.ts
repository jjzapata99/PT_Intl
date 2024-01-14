import express from 'express';

const router = express.Router();
const controller = require('../controllers/auth')

// bajo el path de /auth/createToken, nos sirve para generar un token temporal para tener acceso a las rutas prioritarias
// este metodo post recibe un json con el siguiente formato "username":"Nombre Usuario"

router.post("/createToken", controller.createToken);

module.exports = router;
