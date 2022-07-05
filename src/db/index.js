const mongoose = require('mongoose')


mongoose.connect(
    "mongodb://victor:1@localhost:27017/dizertatie",
    () => {
        console.log("Connection Sucessful!")
    },
    e => console.error(e)
)