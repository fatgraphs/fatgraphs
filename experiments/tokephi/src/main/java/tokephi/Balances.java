package tokephi;

import java.io.FileInputStream;
import java.io.DataInputStream;
import java.util.*;
import java.io.File;

import java.lang.Math;
import java.math.BigInteger;

//d = sqrt(area/pi)*2

public class Balances {

    private Map<String, BigInteger> minBalances = new HashMap<String, BigInteger>();
    private Map<String, BigInteger> maxBalances = new HashMap<String, BigInteger>();
    private BigInteger maxOverallBalance = new BigInteger("0");

    private Map<String, BigInteger> currentBalances = new HashMap<String, BigInteger>();

    private String filePath;
    private String currentLine = null;

    private Scanner currentScanner = null;
    private String[] columns = null;
    private int blockIdx, sourceIdx, targetIdx, amountIdx;
    //private Map<String, BigInteger> dictionary = new HashMap<String, BigInteger>();
    //private Map<String, BigInteger> maxBalances = new HashMap<String, BigInteger>();
    private int minBlock = Integer.MAX_VALUE;
    private int maxBlock = 0;
    private int blockRange = 0;

    private int currentBlock = 0;
    private final BigInteger zero = new BigInteger("0");

    public Balances(String filePath) {
      this.filePath = filePath;
        try {
          this.currentScanner = new Scanner(new File(filePath)); // read file
          this.columns = currentScanner.nextLine().split(","); // parse header
          this.blockIdx = this.sourceIdx = this.targetIdx = this.amountIdx = -1;
          // initialize column indices, so that the order doesn't matter
          for (int i=0; i<columns.length; i++) {
              if (columns[i].equals("blockNumber")) { this.blockIdx = i; }
              if (columns[i].equals("source")) { this.sourceIdx = i; }
              if (columns[i].equals("target")) { this.targetIdx = i; }
              if (columns[i].equals("amount")) { this.amountIdx = i; }
          }

          // initialize current line to first data row
          this.currentLine = currentScanner.nextLine();
        } catch (Exception e) { }

        initialzeFields();

        // run thru whole file, compute min balances, minBlock, maxBlock, range
        // initialize currentBalances with positive min balances
        // copy initial current balances, run thru whole file, compute max balances
        // set maxBalance
    }

    private void processLine(String line, HashMap<String, BigInteger> map) {
      String[] fields = line.split(",");
      int block = Integer.parseInt(fields[blockIdx]);
      String source = fields[sourceIdx];
      String target = fields[targetIdx];
      BigInteger amount = new BigInteger(fields[amountIdx]);

      BigInteger sourceBalance = map.getOrDefault(source, this.zero);
      BigInteger targetBalance = map.getOrDefault(target, this.zero);
      BigInteger newSourceBalance = sourceBalance.subtract(amount);
      BigInteger newTargetBalance = targetBalance.add(amount);
      map.put(source, newSourceBalance);
      map.put(target, newTargetBalance);
    }

    private void initialzeFields() {
      try {
        Scanner firstRunScanner = new Scanner(new File(this.filePath)); // read file
        String[] fields;
        String line, source, target;
        int block;
        BigInteger amount;

        Map<String, BigInteger> localBalances = new HashMap<String, BigInteger>();

        // FIRST RUN - COMPUTE MIN BALANCES ====================================
        firstRunScanner.nextLine(); // Skip the header
        while (firstRunScanner.hasNextLine()) {
          line = firstRunScanner.nextLine();
          //processLine(line, localBalances);
          fields = line.split(",");
          block = Integer.parseInt(fields[blockIdx]);
          source = fields[sourceIdx];
          target = fields[targetIdx];
          amount = new BigInteger(fields[amountIdx]);

          BigInteger sourceBalance = localBalances.getOrDefault(source, this.zero);
          BigInteger targetBalance = localBalances.getOrDefault(target, this.zero);
          BigInteger newSourceBalance = sourceBalance.subtract(amount);
          BigInteger newTargetBalance = targetBalance.add(amount);
          localBalances.put(source, newSourceBalance);
          localBalances.put(target, newTargetBalance);

          if(newSourceBalance.compareTo(this.minBalances.getOrDefault(source, this.zero)) < 0) {
            // newSourceBalance is lower
            this.minBalances.put(source, newSourceBalance);
          }

          if(this.minBlock > block) { this.minBlock = block; }
          if(this.maxBlock < block) { this.maxBlock = block; }
        }
        this.blockRange = this.maxBlock - this.minBlock;
        this.currentBlock = this.minBlock;

        // TAKE MINBALANCES, FLIP THE SIGN AND SET AS INITIAL BALANCES FOR CURRENT BALANCES
        for (Map.Entry<String, BigInteger> entry : minBalances.entrySet()) {
            BigInteger value = entry.getValue();
            if(value.compareTo(this.zero) < 0) {
              this.currentBalances.put(entry.getKey(), value.multiply(new BigInteger("-1")));
            }
        }

        // Compute max localBalances
        localBalances = new HashMap<String, BigInteger>();
        localBalances.putAll(this.currentBalances);
        this.maxBalances.putAll(this.currentBalances);
        firstRunScanner = new Scanner(new File(this.filePath)); // read file again

        firstRunScanner.nextLine(); // Skip the header
        while (firstRunScanner.hasNextLine()) {
          line = firstRunScanner.nextLine();
          fields = line.split(",");
          block = Integer.parseInt(fields[blockIdx]);
          source = fields[sourceIdx];
          target = fields[targetIdx];
          amount = new BigInteger(fields[amountIdx]);

          BigInteger sourceBalance = localBalances.getOrDefault(source, this.zero);
          BigInteger targetBalance = localBalances.getOrDefault(target, this.zero);
          BigInteger newSourceBalance = sourceBalance.subtract(amount);
          BigInteger newTargetBalance = targetBalance.add(amount);
          localBalances.put(source, newSourceBalance);
          localBalances.put(target, newTargetBalance);

          if(newTargetBalance.compareTo(this.maxBalances.getOrDefault(target, this.zero)) > 0) {
            // newTargetBalance is higher
            //System.out.println("Setting a new max("+newTargetBalance+") for "+target);
            this.maxBalances.put(target, newTargetBalance);
          }

          if(this.maxOverallBalance.compareTo(newTargetBalance) < 0) {
            this.maxOverallBalance = newTargetBalance;
          }
        }

      } catch (Exception ex)  { System.out.println(ex); }
    }

    public Map<String, BigInteger> getMaxBalances() {
      return(this.maxBalances);
    }

    public BigInteger getMaxOverallBalance() {
      return(this.maxOverallBalance);
    }

    public int getBlockStart() {
      return(this.minBlock);
    }

    public int getBlockEnd() {
      return(this.maxBlock);
    }

    public int getBlockRange() {
      return(this.blockRange);
    }

    public void goToNextBalanceState(int stepSize) {
      System.out.println("Trying to go to next balance state");
      System.out.println("Step size is " + stepSize);
      System.out.println("Current block is "+ this.currentBlock);
      String[] fields;
      String line, source, target;
      int block;
      BigInteger amount;

      int newBlockLimit = this.currentBlock + stepSize;
      this.currentBlock = newBlockLimit;


      do{
          // process current line
          //System.out.println("Current line is "+ this.currentLine);
          fields = this.currentLine.split(",");
          block = Integer.parseInt(fields[blockIdx]);
          source = fields[sourceIdx];
          target = fields[targetIdx];
          amount = new BigInteger(fields[amountIdx]);

          if(block <= newBlockLimit) {
              BigInteger sourceBalance = this.currentBalances.getOrDefault(source, this.zero);
              BigInteger targetBalance = this.currentBalances.getOrDefault(target, this.zero);
              BigInteger newSourceBalance = sourceBalance.subtract(amount);
              BigInteger newTargetBalance = targetBalance.add(amount);
              this.currentBalances.put(source, newSourceBalance);
              this.currentBalances.put(target, newTargetBalance);

              // read the next line
              this.currentLine = this.currentScanner.nextLine();
          } else {
            //System.out.println("Not processing this line. Block limit is " + newBlockLimit);
            return;
          }
      }while(block <= newBlockLimit && this.currentScanner.hasNextLine());
    }

    public BigInteger getAddressBalance(String address) {
      return(this.currentBalances.getOrDefault(address, this.zero));
    }

    public BigInteger getMaxAddressBalance(String address) {
        return(this.maxBalances.getOrDefault(address, this.zero));
    }

    private int convertBalanceToRadius(BigInteger balance, int maxRadius) {
      int maxArea = (int) (2*Math.PI*maxRadius*maxRadius);
      //System.out.println("maxArea: "+maxArea);
      //System.out.println("maxOverall: "+this.getMaxOverallBalance());
      BigInteger scaler = this.getMaxOverallBalance().divide(new BigInteger(Integer.toString(maxArea)));
      //System.out.println("scaler: "+scaler);
      BigInteger relBalance = balance.divide(scaler);

      int radius = (int)Math.round(Math.sqrt(relBalance.doubleValue()/(2*Math.PI)));
      /*if((radius < 100) & (radius > 0)) {
        System.out.println(radius);
      }*/
      return(radius);
    }

    public int getAddressRadius(String address, int maxRadius) {
      int radius = convertBalanceToRadius(getAddressBalance(address), maxRadius);
      return(radius);
    }

    public int getMaxAddressRadius(String address, int maxRadius) {
      int radius = convertBalanceToRadius(getMaxAddressBalance(address), maxRadius);
      return(radius);
    }

    // on initialization find:
    // - initial localBalances, due to negative balances seen // find maximum negative
    // - optionally pass in initial balances
    // - max values for each address
    // - max overall value
    // - block start, end, range

    // provide functions:
    // goToNextBalanceState()
    // compute / get next balances based on given numeric interval jump
    // compute / get next balances based on percentage jump
    // get address balance
    // get address diameter based on scale
    // TODO: get max balance until current block so far

}
