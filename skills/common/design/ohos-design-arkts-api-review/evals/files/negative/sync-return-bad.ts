// Eval file for rule: 同步方法禁止通过返回值返回方法执行是否成功
// 反例1：通过返回布尔值表示执行是否成功
function createUser(name: string, email: string): boolean {
  if (!name || !email) {
    return false;  // 应抛出异常
  }

  if (emailExists(email)) {
    return false;  // 应抛出异常
  }

  saveToDatabase(new User(name, email));
  return true;
}

// 反例2：通过返回对象中的success字段表示执行是否成功
function deleteUser(userId: string): { success: boolean; error?: string } {
  const user = getUserById(userId);
  if (!user) {
    return { success: false, error: 'User not found' };  // 应抛出异常
  }

  deleteFromDatabase(userId);
  return { success: true };
}

// 反例3：通过返回null表示执行失败
function getUserById(userId: string): User | null {
  const user = queryDatabase(userId);
  if (!user) {
    return null;  // 应抛出异常
  }
  return user;
}

// 反例4：通过返回错误码表示执行失败
function updateUser(userId: string, data: Partial<User>): number {
  const user = getUserById(userId);
  if (!user) {
    return -1;  // 应抛出异常
  }

  if (!validateData(data)) {
    return -2;  // 应抛出异常
  }

  updateDatabase(userId, data);
  return 0;
}

// 反例5：通过返回对象包含错误信息
function transferMoney(from: string, to: string, amount: number): {
  success: boolean;
  result?: TransferResult;
  error?: string;
} {
  if (amount <= 0) {
    return { success: false, error: 'Amount must be positive' };  // 应抛出异常
  }

  if (!hasSufficientBalance(from, amount)) {
    return { success: false, error: 'Insufficient balance' };  // 应抛出异常
  }

  // 执行转账
  deduct(from, amount);
  credit(to, amount);

  return {
    success: true,
    result: {
      transactionId: generateId(),
      from: from,
      to: to,
      amount: amount,
      timestamp: Date.now()
    }
  };
}

// 反例6：混合返回类型
function saveFile(path: string, content: string): boolean | Error {
  try {
    writeToFile(path, content);
    return true;
  } catch (e) {
    return e;  // 应直接抛出异常
  }
}
