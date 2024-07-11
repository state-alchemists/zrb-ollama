// fibonacci.js

// Function to calculate Fibonacci number iteratively
function fibonacci(n) {
    if (n < 0) {
        throw new Error('Input should be a non-negative integer.');
    }
    if (n <= 1) {
        return n;
    }

    let a = 0, b = 1;
    for (let i = 2; i <= n; i++) {
        let temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

// Input number
const number = 10; // Change this value to test with other numbers

// Calculate and log the Fibonacci number
console.log(`Fibonacci number at position ${number} is ${fibonacci(number)}`);
