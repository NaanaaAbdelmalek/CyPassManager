from src.Cyconfig import check_config
import src.CyUi as CyUi
import src.Cydboperation as Cydboperation 
import src.CyMasterPass as cypass 
import src.CyClipboard as CyClipboard 





def main():
    
    # Here we check for Configuration (Database existance and the Master password)
    is_Configured = check_config()

    if (is_Configured == True):
        # Loading logo and Master password authentification 
        CyUi.logo()
        cypass.masterpass_auth()

        # menu of choices


        while True:

            db = Cydboperation.DataBaseOperation()
            print("\n")
            CyUi.menu() 
            choice = input('\nCyPassManager >> ')
            print('\n')

            if choice.lower() == 'a':
                db.add_record()
            elif choice.lower() == 's':
                db.show_all()
            elif choice.lower() == 'd':
                db.delete_record()
            elif choice.lower() == 'r':
                CyClipboard.to_clipboard()
            elif choice.lower() == 'e':
                break
            else:
                print(CyUi.warnning('Enter a valid choice !'))
    else:
        return 0

if __name__ == "__main__":
    main()



    