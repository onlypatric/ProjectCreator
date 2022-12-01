import java.util.Scanner;

/**
 * MainApp
 */
public class MainApp {

    public static void main(String[] args) {
        
        int x;
        boolean o;
        Scanner sc = new Scanner(System.in);

        x=sc.nextInt();
        o=true;
        for (int i = 2; i <= x/2; i++) {
            if(
                x%i==0
            ){
                System.out.println("non è primo");break;
            }
        }
        if(o){
            System.out.println("è primo");
        }
        else{
            System.out.println("non è primo");
        }
        sc.close();
    }
}