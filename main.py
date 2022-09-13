import logging
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO)

API_TOKEN = 'XXXX:XXXX:XXXX:XXXX'

bot = Bot(token=API_TOKEN)

button3 = KeyboardButton("ovoz berish")

keybord1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button3)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Salom. ovoz bering !!!", reply_markup=keybord1)

    class Form(StatesGroup):
        tel = State()
        kod = State()

    @dp.message_handler(text="ovoz berish")
    async def cmd_start(message: types.Message):
        await Form.tel.set()

        driver.get("https://openbudget.uz/oz/boards/6/123478")
        print("successfully !!!")
        sleep(2)
        driver.find_element(By.XPATH, "//img[@src='/_nuxt/img/positive-vote.ca372aa.svg']").click()
        # sleep(1)
        driver.find_element(By.XPATH, "//div[@class='vote-type']").click()

        sleep(1)
        await message.answer("telefon raqamingizni kiriting ?")

    @dp.message_handler(state=Form.tel)
    async def process_name(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['phone_number'] = message.text
        await Form.next()

        sleep(1)
        driver.find_element(By.XPATH, "//input[@id='phone']").send_keys(data['phone_number'])
        sleep(1)
        driver.find_element(By.XPATH, "//button[@class='btn btn-secondary']").click()
        sleep(3)

        try:
            try:
                await message.answer(
                    driver.find_element(By.XPATH, "//p[@style='color: rgb(245, 65, 65); line-height: 17px;']").text)
                await state.finish()
                # driver.quit()
            except:
                await message.answer(driver.find_element(By.XPATH,
                                                         "//h4[@style='text-align: center; padding-top: 32px; font-weight: 600;']").text)
                await state.finish()
                # driver.quit()
        except:
            await message.answer("Telefoningizga yuborilgan sms kodni kiriting !")
            # await state.finish()

    @dp.message_handler(state=Form.kod)
    async def process_name(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['phone_send_code'] = message.text
        await Form.next()

        driver.find_element(By.XPATH, "//input[@class='form-control']").send_keys(data['phone_send_code'])
        sleep(1)
        driver.find_element(By.XPATH, "//button[@class='btn btn-secondary']").click()
        sleep(1)
        try:
            await message.answer(driver.find_element(By.XPATH, "//p[@style='color: red;']").text)
        except:
            await message.answer("muffaqiyatli ro'yxatga olindingiz !!!")
        await state.finish()
        # driver.quit()



executor.start_polling(dp, skip_updates=True)
