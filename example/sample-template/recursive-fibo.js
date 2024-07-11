// fibonacci.js

// Function to calculate Fibonacci number recursively
function fibonacci(n) {
    if (n < 0) {
        throw new Error('Input should be a non-negative integer.');
    }
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Input number
const number = 10; // Change this value to test with other numbers

// Calculate and log the Fibonacci number
console.log(`Fibonacci number at position ${number} is ${fibonacci(number)}`);
