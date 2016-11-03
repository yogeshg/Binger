import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Set;
import java.util.StringTokenizer;
import java.util.TreeSet;

public class printAllLetters {

    public static void main(String args[]) {
	char c;
	for( int i = 0; i < 65536; ++i ) {
		c = (char)i;
		if(Character.isLetter(c)) {
			System.out.println(i);
			System.err.println(c);
		}
		// System.out.printf("%d, %c , isLetter=%b\n",(int)c, c , Character.isLetter(c));
	}
    }
}
