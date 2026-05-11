// Simple test for ArkTS playground
let x: number = 42;
console.log("Value of x:", x);

class Calculator {
    private result: number = 0;

    add(num: number): void {
        this.result += num;
    }

    getResult(): number {
        return this.result;
    }
}

let calc = new Calculator();
calc.add(10);
calc.add(5);
console.log("Calculator result:", calc.getResult());
