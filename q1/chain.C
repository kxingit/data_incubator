{
    const int N = 16; // # of links
    int nEvents = 10000;
    
    int m = 0; // max # of sub chains
    TRandom3 ran;
    ran.SetSeed();
    
    TH1F* hNchains = new TH1F("hNchains", "hNchains", 8, 0, 8);
    for(int num = 0; num < nEvents; num++){
        if(num % (nEvents / 25) == 0)cout << num << "th event " << endl;
        m = 0;
        int n = N;
        bool taken[N] = {0};
        while(n > 0){ // take a link each time
//            cout << num << "th event " << endl;
            int i = N * ran.Rndm();
//            cout << "i = " << i << endl;
            if(taken[i] == 1) continue;
            taken[i] = 1;
            n--;
            int mcurr = 0;
            // calculate # of sub links
            for(int i = 0; i < N - 1; i++){
                if(!taken[i]) continue;
                else if(taken[i] && taken[i+1]){
                    continue;
                }
                else if(taken[i] && !taken[i+1]){
                    mcurr = mcurr + 1;
                }
                else if(taken[7]){
                    mcurr = mcurr + 1;
                }
            }
//            cout << "mcurr = " << mcurr <<endl;
            m = TMath::Max(m, mcurr);
//            cout << "m = " << m << endl;
        }
//        cout << "max # of chains = " << m << endl;
        hNchains->Fill(m);

    }
    hNchains->Draw();
    cout << nEvents << " events" <<endl;
    cout << N << " links" << endl;
    cout << "Mean = " << hNchains->GetMean() << endl;
    cout << "RMS = " << hNchains->GetRMS() << endl;

    TFile *fout = new TFile("result.root","recreate");
    hNchains->Write();
    fout->Write();
    fout->Close();
}

