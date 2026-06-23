// Eval file for rule: 同步方法禁止通过返回值返回方法执行是否成功
// 正例1：成功返回业务结果，失败抛出异常
function createUser(name: string, email: string): User {
  if (!name || !email) {
    throw new Error('Name and email are required');
  }

  if (emailExists(email)) {
    throw new Error('Email already exists');
  }

  const user = new User(name, email);
  saveToDatabase(user);
  return user;
}

// 正例2：void返回类型，失败抛出异常
function deleteUser(userId: string): void {
  const user = getUserById(userId);
  if (!user) {
    throw new Error('User not found');
  }

  deleteFromDatabase(userId);
}

// 正例3：返回业务数据，失败抛出异常
function getUserById(userId: string): User {
  const user = queryDatabase(userId);
  if (!user) {
    throw new Error('User not found');
  }
  return user;
}

// 正例4：返回可选类型，失败抛出异常
function findUserByEmail(email: string): User | null {
  if (!email) {
    throw new Error('Email is required');
  }
  return queryDatabaseByEmail(email);
}

// 正例5：返回布尔值表示业务状态（非执行是否成功）
function hasPermission(userId: string, permission: string): boolean {
  const user = getUserById(userId);
  return user.permissions.includes(permission);
}

// 正例6：返回操作结果对象
function transferMoney(from: string, to: string, amount: number): TransferResult {
  if (amount <= 0) {
    throw new Error('Amount must be positive');
  }

  if (!hasSufficientBalance(from, amount)) {
    throw new Error('Insufficient balance');
  }

  // 执行转账
  deduct(from, amount);
  credit(to, amount);

  return {
    transactionId: generateId(),
    from: from,
    to: to,
    amount: amount,
    timestamp: Date.now()
  };
}
