package tokephi;

import org.junit.Test;
import static org.junit.Assert.*;
import junit.framework.TestCase;

import java.math.BigInteger;

public class BalancesTest extends TestCase {

    private Balances bal;

    @Override
    protected void setUp() throws Exception {
        System.out.println("Setting it up!");
        ClassLoader classLoader = getClass().getClassLoader();
        bal = new Balances(classLoader.getResource("tokenTransfers.csv").getFile());
    }

    @Test public void findStartBlock() {
        assertEquals(bal.getBlockStart(), 5233833);
    }

    @Test public void findEndBlock() {
        assertEquals(bal.getBlockEnd(), 6010127);
    }

    @Test public void testGetMaxOverallBalance() {
        assertEquals(bal.getMaxOverallBalance(), new BigInteger("100000000000000000"));
    }

    @Test public void testAddressRadius() {
        assertEquals(bal.getAddressRadius("0x0000000000000000000000000000000000000000", 1000), 1000);
        assertEquals(bal.getAddressRadius("0xdd2a5b646bb936cbc279cbe462e31eab2c309452", 1000), 0);
        bal.goToNextBalanceState(1000000);
        assertEquals(bal.getAddressRadius("0x0000000000000000000000000000000000000000", 1000), 0);
        assertEquals(bal.getAddressRadius("0xdd2a5b646bb936cbc279cbe462e31eab2c309452", 1000), 1000);
        assertEquals(bal.getAddressRadius("0xa631ec94edce1fe78cd7344a029b6c37c0df7dca", 1000), 5);


    }

    @Test public void testGetAddressBalance() {
        // before processing the transfers, 0x0 should have everything
        assertEquals(bal.getAddressBalance("0x0000000000000000000000000000000000000000"), new BigInteger("100000000000000000"));

        // after processing only 10 blocks nothing should change
        bal.goToNextBalanceState(10);
        assertEquals(bal.getAddressBalance("0x0000000000000000000000000000000000000000"), new BigInteger("0"));
        assertEquals(bal.getAddressBalance("0xdd2a5b646bb936cbc279cbe462e31eab2c309452"), new BigInteger("100000000000000000"));
        bal.goToNextBalanceState(747274);
        assertEquals(bal.getAddressBalance("0xdd2a5b646bb936cbc279cbe462e31eab2c309452"), new BigInteger("99997500000000000"));
    }

    @Test public void testGetMaxBalance() {
        bal.goToNextBalanceState(1);
        assertEquals(new BigInteger("100000000000000000"), bal.getMaxAddressBalance("0x0000000000000000000000000000000000000000"));
        assertEquals(new BigInteger("2500000000000"), bal.getMaxAddressBalance("0xc802506207a588cf85191b14693743d3777add8b"));

    }
}
