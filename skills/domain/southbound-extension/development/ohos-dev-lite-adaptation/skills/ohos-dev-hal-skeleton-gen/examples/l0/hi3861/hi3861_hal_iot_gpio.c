/*
 * Copyright (c) 2020 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "iot_errno.h"
#include "iot_gpio.h"
#include "hi_gpio.h"


#define GPIO_PIN_INIT    1
#define GPIO_PIN_UNINIT  0

static unsigned char g_gpioMap[HI_GPIO_IDX_MAX] = {0};
static unsigned char g_gpioInitNum = 0;

unsigned int IoTGpioInit(unsigned int id)
{
    if (id >= HI_GPIO_IDX_MAX) {
        return IOT_FAILURE;
    }

    if (g_gpioInitNum == 0) {
        (void)hi_gpio_init();
    }

    if (g_gpioMap[id] == GPIO_PIN_INIT) {
        return IOT_FAILURE;
    } else {
        g_gpioMap[id] = GPIO_PIN_INIT;
        g_gpioInitNum++;
    }

    return IOT_SUCCESS;
}

unsigned int IoTGpioSetDir(unsigned int id, IotGpioDir dir)
{
    return hi_gpio_set_dir((hi_gpio_idx)id, (hi_gpio_dir)dir);
}

unsigned int IoTGpioGetDir(unsigned int id, IotGpioDir *dir)
{
    return hi_gpio_get_dir((hi_gpio_idx)id, (hi_gpio_dir *)dir);
}

unsigned int IoTGpioSetOutputVal(unsigned int id, IotGpioValue val)
{
    return hi_gpio_set_ouput_val((hi_gpio_idx)id, (hi_gpio_value)val);
}

unsigned int IoTGpioGetOutputVal(unsigned int id, IotGpioValue *val)
{
    return hi_gpio_get_output_val((hi_gpio_idx)id, (hi_gpio_value *)val);
}

unsigned int IoTGpioGetInputVal(unsigned int id, IotGpioValue *val)
{
    return hi_gpio_get_input_val((hi_gpio_idx)id, (hi_gpio_value *)val);
}

unsigned int IoTGpioRegisterIsrFunc(unsigned int id, IotGpioIntType intType, IotGpioIntPolarity intPolarity,
                                    GpioIsrCallbackFunc func, char *arg)
{
    return hi_gpio_register_isr_function((hi_gpio_idx)id, (hi_gpio_int_type)intType,
                                         (hi_gpio_int_polarity)intPolarity, (gpio_isr_callback)func, arg);
}

unsigned int IoTGpioUnregisterIsrFunc(unsigned int id)
{
    return hi_gpio_unregister_isr_function((hi_gpio_idx)id);
}

unsigned int IoTGpioSetIsrMask(unsigned int id, unsigned char mask)
{
    return hi_gpio_set_isr_mask((hi_gpio_idx)id, (hi_bool)mask);
}

unsigned int IoTGpioSetIsrMode(unsigned int id, IotGpioIntType intType, IotGpioIntPolarity intPolarity)
{
    return hi_gpio_set_isr_mode((hi_gpio_idx)id, (hi_gpio_int_type)intType, (hi_gpio_int_polarity)intPolarity);
}

unsigned int IoTGpioDeinit(unsigned int id)
{
    if (id >= HI_GPIO_IDX_MAX) {
        return IOT_FAILURE;
    }

    if (g_gpioMap[id] == GPIO_PIN_INIT) {
        g_gpioInitNum--;
        g_gpioMap[id] = GPIO_PIN_UNINIT;
    } else {
        return IOT_FAILURE;
    }

    if (g_gpioInitNum == 0) {
        return hi_gpio_deinit();
    } else {
        return IOT_SUCCESS;
    }
}

