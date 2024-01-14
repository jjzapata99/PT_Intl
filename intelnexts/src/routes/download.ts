import express from 'express';
const auth = require("../controllers/auth")
const router = express.Router();
const controller = require('../controllers/download')

// bajo el path /download/downloadPDF

router.get("/downloadPDF", auth.authenticateToken,controller.downloadSign);

module.exports = router;