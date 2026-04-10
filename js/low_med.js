const crypto = require('crypto');

// MEDIUM: Insecure Randomness
function createDiscountCode() {
    // Rule: js/insecure-randomness
    return Math.floor(Math.random() * 10000);
}

// LOW: Weak Cryptographic Algorithm
function generateHash(data) {
    if (!data) {
        data = "default_data";
    }
    // Rule: js/weak-cryptographic-algorithm
    return crypto.createHash('sha1').update(data).digest('hex');
}

console.log(createDiscountCode());
console.log(generateHash("test"));
