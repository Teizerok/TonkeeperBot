from pytonapi import AsyncTonapi
from tonsdk.utils import bytes_to_b64str, to_nano
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
import os
from dotenv import load_dotenv
from TonTools import *
from consts.configuration import jetonDictionary

load_dotenv()

API_KEY = os.getenv('TON_API_KEY')
MNEMONICS = os.getenv('MNEMONICS')


class TransferMethod:
    async def __transferTon(self, address, amount, mnemonics):
        try:
            tonapi = AsyncTonapi(api_key=API_KEY, is_testnet=False)

            mnemonics_list = mnemonics.split(
                " ") if mnemonics else MNEMONICS.split(" ")
            _mnemonics, _pub_k, _priv_k, wallet = Wallets.from_mnemonics(
                mnemonics_list,
                WalletVersionEnum.v4r2,
                0,
            )

            method_result = await tonapi.blockchain.execute_get_method(
                wallet.address.to_string(False), "seqno"
            )
            seqno = int(method_result.decoded.get("state", 0))

            transfer_amount = to_nano(float(amount), 'ton')

            query = wallet.create_transfer_message(
                to_addr=address,
                amount=transfer_amount,
                payload=None,
                seqno=seqno,
            )

            message_boc = bytes_to_b64str(query["message"].to_boc(False))
            data = {'boc': message_boc}
            await tonapi.blockchain.send_message(data)
        except Exception as _:
            print(f"Error in transfer ton method for account {address}")
            raise

    async def __transferJeton(self, address, amount, jeton, mnemonics):
        try:
            client = TonCenterClient(orbs_access=True)
            mnemonics_list = mnemonics.split(
                " ") if mnemonics else MNEMONICS.split(" ")

            your_wallet = Wallet(
                provider=client, mnemonics=mnemonics_list, version='v4r2')

            await your_wallet.transfer_jetton(
                destination_address=address,
                jetton_master_address=jetonDictionary[jeton],
                jettons_amount=float(amount)
            )
        except Exception as _:
            print(f"Error in transfer jeton method for account {address}")
            raise

    async def transferMethod(self, address, amount, jeton, mnemonics=None):
        if not isinstance(address, str):
            print('Write correct account.')
            return

        if not isinstance(amount, (str, int, float)):
            print('Write correct amount.')
            return

        if jeton == 'ton':
            await self.__transferTon(address, amount, mnemonics)
        elif jeton in jetonDictionary:
            await self.__transferJeton(address, amount, jeton, mnemonics)
        else:
            print('This token is not registered, try another.')
            return
