import express from 'express';
const router = express.Router()

// Se definen todas las rutas y dentro de cada archivo de ruta correspondiente se implementa su controlador

const routes = [
    {
        path: 'download'
    },
    {
        path: 'upload'
    },
    {
        path:"auth"
    }
]

routes.forEach(route => {
    return router.use(`/${route.path}`, require(`./${route.path}`))
})

module.exports = router