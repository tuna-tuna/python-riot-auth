import asyncio
import sys
from concurrent.futures import ThreadPoolExecutor

import riot_auth

# region asyncio.run() bug workaround for Windows, remove below 3.8 and above 3.10.6
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# endregion

async def inputMFACode() -> str:
    """
    asyncio version input
    """
    mfaCode: str = ''
    with ThreadPoolExecutor(1, 'inputMFACode') as e:
        return (await asyncio.get_event_loop().run_in_executor(e, input, mfaCode)).rstrip()

async def main():
    CREDS = "USERNAME", "PASSWORD"
    auth = riot_auth.RiotAuth()
    try:
        result = await auth.authorize(*CREDS)
        # No MFA
        if result == 'Success':
            print('No MFA, Successfully Authorized')
            print(f"Access Token Type: {auth.token_type}\n")
            print(f"Access Token: {auth.access_token}\n")
            print(f"Entitlements Token: {auth.entitlements_token}\n")
            print(f"User ID: {auth.user_id}")

        # MFA
        elif result == 'MFA':
            mfaCode = await inputMFACode()
            mfaResult = await auth.mfa(mfaCode)
            if mfaResult == 'Success':
                print('Successfully Authorized with MFA')
                print(f"Access Token Type: {auth.token_type}\n")
                print(f"Access Token: {auth.access_token}\n")
                print(f"Entitlements Token: {auth.entitlements_token}\n")
                print(f"User ID: {auth.user_id}")

        await asyncio.sleep(5)
        
        # Reauth
        result = await auth.reauthorize()
        print('Successfully Re-Authorized')
        print(f"Access Token Type: {auth.token_type}\n")
        print(f"Access Token: {auth.access_token}\n")
        print(f"Entitlements Token: {auth.entitlements_token}\n")
        print(f"User ID: {auth.user_id}")

    except Exception as e:
        print('Error')
        print(e)

asyncio.run(main())