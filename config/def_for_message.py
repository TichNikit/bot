import aiosqlite


async def add_user(id, full_name, username):
    connect = await aiosqlite.connect('db.db')
    cursor = await connect.cursor()
    await cursor.execute('INSERT INTO users (id, full_name, username, calorie_allowance, your_calorie, income)'
                         ' VALUES (?, ?, ?, ?, ?, ?)',
                         (id, full_name, username, 0, 0, 0))
    await connect.commit()
    await cursor.close()
    await connect.close()


async def user_exists(user_id):
    connect = await aiosqlite.connect('db.db')
    cursor = await connect.cursor()
    await cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = await cursor.fetchone()
    await cursor.close()
    await connect.close()
    return user is not None


async def calories_to_db(calories, user_id):
    connect = await aiosqlite.connect('db.db')
    cursor = await connect.cursor()
    await cursor.execute('UPDATE users SET calorie_allowance = ? WHERE id = ?', (calories, user_id))
    await connect.commit()
    await cursor.close()
    await connect.close()


async def insert_or_update_calories(calories, user_id):
    connect = await aiosqlite.connect('db.db')
    cursor = await connect.cursor()
    await cursor.execute('SELECT your_calorie FROM users WHERE id = ?', (user_id,))
    add_calorie = await cursor.fetchone()

    fold_calorie = add_calorie[0]
    fold_calorie_2 = fold_calorie + calories
    await cursor.execute('UPDATE users SET your_calorie = ? WHERE id = ?', (fold_calorie_2, user_id))
    await connect.commit()
    await cursor.close()
    await connect.close()



async def calorie_analysis(user_id):
    connect = await aiosqlite.connect('db.db')
    cursor = await connect.cursor()
    await cursor.execute('SELECT calorie_allowance FROM users WHERE id = ?', (user_id,))
    all_calorie = await cursor.fetchone()
    all_calorie = all_calorie[0]
    await cursor.execute('SELECT your_calorie FROM users WHERE id = ?', (user_id,))
    norm_calorie = await cursor.fetchone()
    norm_calorie = norm_calorie[0]
    await connect.commit()
    await cursor.close()
    await connect.close()
    return [norm_calorie, all_calorie]


async def delete_all_calories(user_id):
    connect = await aiosqlite.connect('db.db')
    cursor = await connect.cursor()
    await cursor.execute('UPDATE users SET your_calorie = ? WHERE id = ?', (0, user_id))
    await connect.commit()
    await cursor.close()
    await connect.close()


async def add_new_income(income, user_id):
    connect = await aiosqlite.connect('db.db')
    cursor = await connect.cursor()

    await cursor.execute('SELECT income FROM users WHERE id = ?', (user_id,))
    add_income = await cursor.fetchone()
    add_income = add_income[0]


    add_income_sum = add_income + income
    await cursor.execute('UPDATE users SET income = ? WHERE id = ?', (add_income_sum, user_id))
    data = add_income_sum
    await connect.commit()
    await cursor.close()
    await connect.close()
    return data


async def add_new_expenses(income, user_id):
    connect = await aiosqlite.connect('db.db')
    cursor = await connect.cursor()

    await cursor.execute('SELECT income FROM users WHERE id = ?', (user_id,))
    add_expenses = await cursor.fetchone()
    add_expenses = add_expenses[0]

    add_expenses_sum = add_expenses - income
    await cursor.execute('UPDATE users SET income = ? WHERE id = ?', (add_expenses_sum, user_id))
    data = add_expenses_sum
    await connect.commit()
    await cursor.close()
    await connect.close()
    return data

async def delete_all_income(user_id):
    connect = await aiosqlite.connect('db.db')
    cursor = await connect.cursor()
    await cursor.execute('UPDATE users SET income = ? WHERE id = ?', (0, user_id))
    await connect.commit()
    await cursor.close()
    await connect.close()