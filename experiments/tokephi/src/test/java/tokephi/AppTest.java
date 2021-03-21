/*
 * This Java source file was generated by the Gradle 'init' task.
 */
package tokephi;

import org.junit.Test;
import static org.junit.Assert.*;

public class AppTest {

    @Test public void testAppFindsMaxBlockInBalances() {
        ClassLoader classLoader = getClass().getClassLoader();
        Balances bal = new Balances(classLoader.getResource("tokenTransfers.csv").getFile());
        assertEquals(bal.getBlockEnd(), 6010127);
    }
}