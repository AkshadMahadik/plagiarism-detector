const express = require("express");
const cors = require("cors");
const multer = require("multer");
const axios = require("axios");
const fs = require("fs");
const FormData = require("form-data");

const app = express();
const port = 5000;

app.use(cors());
app.use(express.json());

// Multer setup for file uploads
const upload = multer({ dest: "uploads/" });

// 🔧 Fix: Change field name to "files" to match frontend
app.post("/upload", upload.single("files"), async (req, res) => {
  try {
    const filePath = req.file.path;
    const fileName = req.file.originalname;

    const formData = new FormData();
    formData.append("file", fs.createReadStream(filePath), fileName); // 👈 FastAPI still expects "file"

    const response = await axios.post("http://localhost:8000/extract", formData, {
      headers: formData.getHeaders(),
    });

    fs.unlinkSync(filePath); // Clean up temp file

    res.json({ extractedText: response.data.text });
  } catch (err) {
    console.error("Error forwarding file to NLP service:", err.message);
    res.status(500).json({ error: "Failed to extract text" });
  }
});

app.listen(port, () => {
  console.log(`Express server running at http://localhost:${port}`);
});
