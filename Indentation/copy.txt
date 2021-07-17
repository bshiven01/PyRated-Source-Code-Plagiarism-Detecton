// Shiven Modified GS OpenMP
#include <omp.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <iostream>
#include <iomanip>

using namespace std;

double *A,*A_copy,*Q,*R;            //Representative matrices for QR factorization 
double *qr, *qqt;                         //qr= (Q x R)
int n;                              //size of matrix

void initvector(int *vector, int m);
void randmatrixcopy(double *mat, double *copymat, int m);

int main() 
{
	int i,j,k;
    int thread_id,num_threads;
	int qr_eval=1,prt_mat=1;        //Flags variables for printing matrix and evaluating error                                             
    double norm_error;              //Norm of error in evaluation i.e e=QR-A
    double exec_time;               //Execution time
    int *step;                      //stores information on which column has been modified
   
	n=10;                          //set matrix size                                                
	
    num_threads = 16;                //number of parallel threads       
	
    omp_set_num_threads(num_threads);	
  
   	/* Allocate memory for (n*n) 1D arrays */  
   	A = (double *)malloc(n*n*sizeof(double));
   	A_copy = (double *)malloc(n*n*sizeof(double));
   	Q = (double *)malloc(n*n*sizeof(double));
   	R = (double *)malloc(n*n*sizeof(double));	   	
   
    step=(int *)malloc(n*sizeof(int));

    initvector(step,n);             //initializa all values to 0

	exec_time=omp_get_wtime();      //Start counting execution time
	double r_sq = 0;               //stores squares of elements of R

    srand(time(0));

	#pragma omp parallel private(i,j,k,r_sq,thread_id)
	{
		thread_id=omp_get_thread_num();

        /* Generate random matrix and a copy*/

        randmatrixcopy(A,A_copy,n);
	
		/* Implementation of Modified GS: A is iteratively modified by matrix transformations to yield a upper triangular matrix */
	
		/* Thread 0 calculates the first column of Q,R */
		r_sq=0;
		if(thread_id==0)
		{
			for (i=0; i<n; i++){			
				r_sq = r_sq + A[0*n+i] * A[0*n+i]; 
			}
			R[0*n+0] = sqrt(r_sq);  			
			for (i=0; i<n; i++) {
				Q[0*n+i] = A[0*n+i]/R[0*n+0];							
	      	}
	      	step[0]=1;
		}

        /* Calculated k_th column of Q,R */
	    for (k=1; k<n; k++)
	    {	    	   	
			step[k-1]=1;                    //Check if previous column is computed
	  		#pragma omp for 
		    for(j=0; j<n; j++)
		    {	
		    	if(j>=k)
		    	{	    	
			        R[(k-1)*n+j]=0;	
			        for(i=0; i<n; i++) {			        	
			        	R[j*n+(k-1)] += Q[(k-1)*n+i] * A[j*n+i];                //Update R (non-diagonal)			        	
			        } 
			        for (i=0; i<n; i++) {				        	
			        	A[j*n+i] = A[j*n+i] - R[j*n+(k-1)]*Q[(k-1)*n+i];        //Update A (final A should be upper triangular)
			        }			        
			       
					if(j==k)
					{
						thread_id=omp_get_thread_num();
						r_sq=0;
						for (i=0; i<n; i++){			
							r_sq = r_sq + A[k*n+i] * A[k*n+i]; 
						}
						R[k*n+k] = sqrt(r_sq);                                 //Update R (diagonal) 			

						for (i=0; i<n; i++) {
							Q[k*n+i] = A[k*n+i]/R[k*n+k];                       //Update Q			
				      	}
				      	step[k-1]=0;
                        step[k]=1;                                              
			      	}
		      	}		        
			}			
			r_sq=0;	      	
		}
	}
	exec_time=omp_get_wtime()-exec_time;                                        //Calculate execution time 

   	// Evaluate results 

   	qqt = (double *)malloc(n*n*sizeof(double));   	

   	if(prt_mat==1) {
   		/*printf("\nEvaluating A...\n");
		for (i = 0; i<n; i++){
		  	for(j=0;j<n;j++){			  	
			  	//printf("%.3f ", A_copy[j*n+i]);
		  	}
		  	//printf("\n");
		}*/

		printf("\nEvaluating Q...\n");
		for (i = 0; i<n; i++){
		  	for(j=0;j<n;j++){			  	
			  	printf("%.3f ", Q[j*n+i]);
		  	}
		  	printf("\n");
		}

		/*printf("\nEvaluating R...\n");
		for (i = 0; i<n; i++){
		  	for(j=0;j<n;j++){			  	
			  	//printf("%.3f ", R[j*n+i]);
		  	}
		  	//printf("\n");
		}*/			
	}	
	
	//Evaluating the decomposition
	 
	if(qr_eval==1){
		/*for (i = 0; i < n; i++) {
			for (j = 0; j < n; j++) {
				sum = 0;
				for (k = 0; k < n; k++) {
					sum = sum + Q[k*n+i] * R[j*n+k];
				}
				qr[j*n+i] = sum;
			}
		}*/

        double sum=0;
        for(i=0;i<n;i++)
        {            
            for(j=0;j<n;j++)
            {
                for(k=0;k<n;k++)
                {
                    sum+=Q[k*n+i]*Q[j*n+k];                    
                }
                qqt[j*n+i]=sum;               
            }            
        }

        double error=0;   
        for(i=0;i<n;i++)
        {            
            for(j=0;j<n;j++)
            {
                if(j==i)
                {
                    //for(k=0;k<n;k++)
                    {
                    error+=error+qqt[j*n+i];                                                        
                    }                        
                }         
                               
            }            
        }
        error=sqrt(n-error);
        cout<<endl<<"Error is "<<error<<endl;

        
		/*if(prt_mat==1){
		printf("\nEvaluating Q*R... \n");
			for (i = 0; i < n; i++) {
				for (j = 0; j < n; j++) {
					//printf("%.3f ", qr[j*n+i]);
				}
				//printf("\n");
			}
		}
		norm_error=0;
        cout<<endl<<"Evaluating error..."<<endl;
		for (i = 0; i < n; i++) {
			for (j = 0; j < n; j++) {				
				norm_error+=fabs(qr[j*n+i]-A_copy[j*n+i]);
			}			
		}
		printf("\nError: %e\n",norm_error);*/
	}

    cout<<endl<<"Execution time (in sec): "<<exec_time<<endl;
    cout<<endl<<"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Prog End %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"<<endl;

    //free memory
	free(A);
    free(A_copy);
    free(Q);
    free(R);
    free(qr);
    free(step);
    free(qqt);
	
    return 0;
}

void initvector(int *vector, int m)
{
    for(int iter=0;iter<m;iter++)
    {
        vector[iter]=0;

    }

}

void randmatrixcopy(double *mat, double *copymat, int m)
{
    int iter1, iter2;
    #pragma omp for
    for(iter1=0;iter1<m;iter1++)
    {
        for(iter2=0;iter2<m;iter2++)
        {
            mat[iter1*m+iter2]=rand()%10;
            copymat[iter1*m+iter2]=mat[iter1*m+iter2];
        }
    }

}
