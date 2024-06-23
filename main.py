from modules.transferModule import TransferMethod
import asyncio
from consts.configuration import AGREEMENT_PHRASE, ACCOUNT_STATUSES, TIME_DELAY


async def sendToWalletAccount():
    answer = input(f'Write "{AGREEMENT_PHRASE}" to continue: ')
    if answer != AGREEMENT_PHRASE:
        print('Sorry... try again.')
        return
    print('Program has been started')

    try:
        with open('data.csv', 'r') as accountList:
            for accountData in accountList:
                accountInfo = accountData.split(',')
                if accountInfo[0] == ACCOUNT_STATUSES[0]:
                    try:
                        transferMethod = TransferMethod()
                        address, amount, token = accountInfo[1:4]
                        mnemonics = accountInfo[4].replace('\n', '') if len(
                            accountInfo) > 4 else None

                        await transferMethod.transferMethod(address, amount, token, mnemonics)
                        await asyncio.sleep(TIME_DELAY)
                    except Exception as _:
                        print(f"Error processing account {
                              accountInfo[1]}")
                        raise
                elif accountInfo[0] == ACCOUNT_STATUSES[1]:
                    continue
                else:
                    print(f"{accountInfo[1]} has not a valid status")
            print('Program was successfully executed.')
    except Exception as e:
        print(f"Something went wrong, ooops...!: {e}")

    finally:
        print('end.')

asyncio.run(sendToWalletAccount())
