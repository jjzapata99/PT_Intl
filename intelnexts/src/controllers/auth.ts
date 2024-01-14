import dotenv from 'dotenv';
const jwt = require('jsonwebtoken');
dotenv.config();

// Genera un token temporal segun las variables asignadas

function generateAccessToken(username:any) {
    return jwt.sign(username, process.env.TOKEN_SECRET, { expiresIn: `${process.env.EXPIRE_TOKEN}m` });
}

// Verifica la validez del token

exports.authenticateToken = (req: any, res:any, next:any) => {
    const authHeader = req.headers['authorization']
    const token = authHeader && authHeader.split(' ')[1]

    if (token == null) return res.sendStatus(401)

    jwt.verify(token, process.env.TOKEN_SECRET as string, (err: any, user: any) => {

        if (err) return res.sendStatus(403)

        req.user = user

        next()
    })
}

// Crea un token a partir de un usuario, hace falta la implementación del manejo de usuarios con una base de datos

exports.createToken =(req: any, res:any) => {
    const token = generateAccessToken({ username: req.body.username });
    res.json(token);
}