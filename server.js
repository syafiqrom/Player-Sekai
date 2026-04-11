const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = 3000;

app.use(express.static(__dirname));

// Serve the songs folder statically
app.use("/songs", express.static(path.join(__dirname, "songs")));

// Endpoint to get list of songs
app.get("/api/songs", (req, res) => {
  const songsDir = path.join(__dirname, "songs");

  function getAllMp3Files(dir) {
    let results = [];
    const items = fs.readdirSync(dir, { withFileTypes: true });

    for (const item of items) {
      const fullPath = path.join(dir, item.name);

      if (item.isDirectory()) {
        results = results.concat(getAllMp3Files(fullPath));
      } else if (item.name.toLowerCase().endsWith(".mp3")) {
        // return relative path for frontend use
        const relativePath = path.relative(songsDir, fullPath).replace(/\\/g, "/");
        results.push(relativePath);
      }
    }

    return results;
  }

  try {
    const mp3Files = getAllMp3Files(songsDir);
    res.json(mp3Files);
  } catch (err) {
    res.status(500).json({ error: "Cannot read songs folder" });
  }
});

// Serve the webpage
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});