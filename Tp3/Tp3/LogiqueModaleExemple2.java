/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.mavenproject1;

import java.io.IOException;
import org.tweetyproject.commons.ParserException;
import org.tweetyproject.logics.fol.syntax.FolFormula;
import org.tweetyproject.logics.ml.parser.MlParser;
import org.tweetyproject.logics.ml.reasoner.SimpleMlReasoner;
import org.tweetyproject.logics.ml.syntax.MlBeliefSet;

/**
 *
 * @author Dell
 */
public class LogiqueModaleExemple2 {
    
     public static void main(String[] args) throws ParserException, IOException {
		// Parse simple BeliefBase from file
		MlParser parser = new MlParser();
		MlBeliefSet b1 = parser.parseBeliefBaseFromFile("C:\\Users\\Dell\\Documents\\NetBeansProjects\\mavenproject1\\src\\main\\java\\com\\mycompany\\mavenproject1\\beliefbase.mlogic");
		FolFormula f1 = (FolFormula) parser.parseFormula("<>(P)");//<>(A&&P)
		System.out.println("Parsed belief base:" + b1 + "\nSignature of belief base:" + b1.getMinimalSignature());
		System.out.println("Parsed formula:" + f1);
                
                SimpleMlReasoner reasoner = new SimpleMlReasoner();
		System.out.println("Answer to query: " + reasoner.query(b1, f1));
}
}