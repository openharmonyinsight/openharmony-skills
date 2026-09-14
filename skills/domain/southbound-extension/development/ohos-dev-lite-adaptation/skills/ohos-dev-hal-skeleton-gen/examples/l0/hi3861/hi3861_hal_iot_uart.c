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
#include "iot_uart.h"
#include "hi_uart.h"

unsigned int IoTUartInit(unsigned int id, const IotUartAttribute *param)
{
    hi_uart_attribute attr = {0};
    hi_uart_extra_attr extraAttr = {0};

    if (NULL == param) {
        return IOT_FAILURE;
    }

    attr.baud_rate = param->baudRate;
    attr.data_bits = param->dataBits;
    attr.pad = param->pad;
    attr.parity = param->parity;
    attr.stop_bits = param->stopBits;

    if (IOT_UART_BLOCK_STATE_NONE_BLOCK == param->rxBlock) {
        extraAttr.rx_block = HI_UART_BLOCK_STATE_NONE_BLOCK;
    } else {
        extraAttr.rx_block = HI_UART_BLOCK_STATE_BLOCK;
    }

    if (IOT_UART_BLOCK_STATE_NONE_BLOCK == param->txBlock) {
        extraAttr.tx_block = HI_UART_BLOCK_STATE_NONE_BLOCK;
    } else {
        extraAttr.tx_block = HI_UART_BLOCK_STATE_BLOCK;
    }

    return hi_uart_init((hi_uart_idx)id, &attr, &extraAttr);
}

int IoTUartRead(unsigned int id, unsigned char *data, unsigned int dataLen)
{
    return hi_uart_read((hi_uart_idx)id, data, dataLen);
}

int IoTUartWrite(unsigned int id, const unsigned char *data, unsigned int dataLen)
{
    return hi_uart_write((hi_uart_idx)id, data, dataLen);
}

unsigned int IoTUartDeinit(unsigned int id)
{
    return hi_uart_deinit((hi_uart_idx)id);
}

unsigned int IoTUartSetFlowCtrl(unsigned int id, IotFlowCtrl flowCtrl)
{
    return hi_uart_set_flow_ctrl((hi_uart_idx)id, (hi_flow_ctrl)flowCtrl);
}
