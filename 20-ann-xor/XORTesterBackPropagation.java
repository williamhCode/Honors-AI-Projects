
/**
 * This class is a small demo that shows how Neuroph
 * works and how ANN work in general.
 * 
 * ANN -Artificial Neural Network
 * 
 * This an XOR gate.
 *    Remember that we could not train an XOR to a Perceptron, right ? 
 * 
 * @author Dr. Carlos Delgado
 *         Based on Neuroph's XOR Tutorial
 * @version April 2015 -- April 2021
 */

import java.util.Arrays;
import org.neuroph.core.NeuralNetwork;
import org.neuroph.nnet.MultiLayerPerceptron;
import org.neuroph.core.data.DataSet;
import org.neuroph.core.data.DataSetRow;
import org.neuroph.util.TransferFunctionType;
import org.neuroph.nnet.learning.BackPropagation;


public class XORTesterBackPropagation

{
   /**
    *   Main method where we do our stuff.
    */ 
   public static void main (String args []) {

    System.out.println ("Backpropagation example by Dr. Carlos Delgado TAS 2015-2021");
    System.out.println ("   based on the MLP XOR Neuroph tutorial");
    // Create Learning Rule. Good old Backpropagation.
    BackPropagation rule = new BackPropagation ();
    rule.setMaxError (0.00001);  // Change this value to show my Students iteration and Max error 
    rule.setMaxIterations(100000); // Usually a big number.
    rule.setLearningRate(1);
    


    // create training set (logical XOR function)
    DataSet trainingSet = new DataSet(2, 1);  // Two inputs and one output
    trainingSet.addRow(new DataSetRow(new double[]{0, 0}, new double[]{0}));
    trainingSet.addRow(new DataSetRow(new double[]{0, 1}, new double[]{1}));
    trainingSet.addRow(new DataSetRow(new double[]{1, 0}, new double[]{1}));
    trainingSet.addRow(new DataSetRow(new double[]{1, 1}, new double[]{0}));

    // create multi layer perceptron  
    // Parameter in the contructor 
    //     Transfer function -- common Sigmoid and Tanh
    //     Nodes in Input layer      
    //     Node in Hidden Layer(s)
    //     Nodes in Output Layer
    
    MultiLayerPerceptron myMlPerceptron = new MultiLayerPerceptron(TransferFunctionType.SIGMOID, 2, 10, 1);
    
    // learn the training set  -- This is where "magic" happens!
    myMlPerceptron.learn(trainingSet, rule);

    // test perceptron -- and hope for the best!
    System.out.println("Testing trained neural network");
    testNeuralNetwork(myMlPerceptron, trainingSet);

    // save trained neural network (this is a good idea for big projects)!
    myMlPerceptron.save("myMlPerceptron.nnet");

    // load saved neural network (test that we saved the network)
    NeuralNetwork loadedMlPerceptron = NeuralNetwork.createFromFile("myMlPerceptron.nnet");

    // test loaded neural network (finally test loaded Network)
    System.out.println("Testing loaded neural network");
    testNeuralNetwork(loadedMlPerceptron, trainingSet);
    
    // Finally print out some details. Play with error and learning!
    System.out.println("Total Error : "+ rule.getTotalNetworkError());
    System.out.println("# Iterations: "+ rule.getCurrentIteration());

}

public static void testNeuralNetwork(NeuralNetwork nnet, DataSet testSet) {

    for(DataSetRow dataRow : testSet.getRows()) {

        nnet.setInput(dataRow.getInput());
        nnet.calculate();
        double[ ] networkOutput = nnet.getOutput();
        System.out.print("Input: " + Arrays.toString(dataRow.getInput()) );
        System.out.println(" Output: " + Arrays.toString(networkOutput) ); 

    }

}
}
