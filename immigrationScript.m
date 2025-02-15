%% Import data from https://tracreports.org/immigration/reports/judgereports/
baseURL = "https://tracreports.org/immigration/reports/judgereports/";
tab = readtable(baseURL,"FileType","html",...
    TableSelector="//TABLE[contains(.,'Immigration Court')]");
% Fill in court data for all rows
ind0 = find(~ismissing(tab.Var1));
ind1 = [ind0(2:end)-1;numel(tab.Var1)];
for j = 1:numel(ind0)
    tab.Var1(ind0(j):ind1(j)) = tab.Var1(ind0(j));
end
%
court = categorical(tab.Var1);
judge = tab.Var2;
total = tab.("Asylum Decisions");
asylum = tab.("Asylum Decisions_1");
other = tab.("Asylum Decisions_2");
denied = tab.("Asylum Decisions_3");

%%  
numJudges = histcounts(court);
courts = unique(court); % better this way than cell array from histcounts
% figure; histogram(court)

%% Get total cases per court
numCases = nan(numel(courts),1);
for j = 1:numel(courts)
    numCases(j) = sum(total(court==courts(j)));
end

%% Get big courts
% judgeThreshold = 30;
% bigCourt = courts(numJudges>judgeThreshold);

caseThreshold = 7500; % top ten
% caseThreshold = 10000; % top five
% caseThreshold = 15000; % top three
bigCourt = courts(numCases>caseThreshold);

%%
colorDenied = [44,105,113]/255;
colorOther = [231,240,241]/255;
colorGranted = [74,167,160]/255;%[20,57,61]/255;

%% Loop over big courts
for j = 1:numel(bigCourt)
    ind = find(court==bigCourt(j));
    label = judge(ind);
    %% Take a pointer from https://www.mathworks.com/matlabcentral/answers/538427
    try
        figure('Position',[0,0,560,210]);
        x = total(ind);
        x_points = movmean(cumsum([0;x]),2,'Endpoints','discard');
        b = gobjects(1,numel(x_points));
        ax = axes();
        hold(ax);
        for k = 1:numel(ind)
            patch(x_points(k)+[-1,-1,1,1]*x(k)/2,...
                denied(ind(k))*[0,1,1,0],...
                colorDenied);
            patch(x_points(k)+[-1,-1,1,1]*x(k)/2,...
                denied(ind(k))+other(ind(k))*[0,1,1,0],...
                colorOther);
            patch(x_points(k)+[-1,-1,1,1]*x(k)/2,...
                denied(ind(k))+other(ind(k))+asylum(ind(k))*[0,1,1,0],...
                colorGranted);        
        end
        % Implicitly deprecated but retained
        foo = x_points/max(x_points);
        bar = diff([0;foo(:)]);
        localThreshold = quantile(bar,(numel(bar)-10)/numel(bar));
        moreCases = find(bar>localThreshold);
        lessCases = find(bar<=localThreshold);
        label(lessCases) = "";
        %
        assert(sum(x)==x_points(end)+x(end)/2,"bad arithmetic");
        axis([0,sum(x),0,100]);
        xlabel("bar width indicates relative asylum caseload of each judge");%,"Interpreter","latex");
        xticks([]);
        ylabel(["percentage of asylum decisions","by each judge"]);%,"Interpreter","latex");
        ax.FontSize = 12;
        %
        fooDenied = plot(nan,nan,'color',colorDenied,'LineWidth',6);
        fooOther = plot(nan,nan,'color',colorOther,'LineWidth',6);
        fooAsylum = plot(nan,nan,'color',colorGranted,'LineWidth',6);
        legend([fooDenied,fooOther,fooAsylum],...
            {'asylum denied','other relief','asylum granted'},...
            'Location','southwest');%,'Interpreter','latex');
        title(join([string(bigCourt(j))," immigration court FY 2018-2024 (",num2str(int64(sum(x)))," cases)"],""));%,'Interpreter','latex');
        % Get Lato at https://fonts.google.com/specimen/Lato and install...
        if ismember("Lato",string(listfonts))
            fontname("Lato");
        end
        %
        box on;
        %
        fileName = join(["Court",strrep(string(bigCourt(j))," ","_"),".png"],"");
        print(fileName,'-r600','-dpng');
    end
end

%%
html = webread(baseURL);

%%
% Links to judge pages are of the following form, so it is unnecessary to
% downselect from something like, e.g. 
    % regexp(html,'<a.*?>','match');
% or even
    % regexp(html,'href="\w{8}/index.html"','match');
link = string(regexp(html,'\w{8}/index.html','match'));
link = link(:);
assert(numel(link)==numel(judge),"numel(links)=numel(judge)");

%% Now dig into judges in big courts
country = cell(numel(bigCourt),1);
percentage = cell(numel(bigCourt),1);
allCountriesBeforeCourt = cell(numel(bigCourt),1);
countryDistribution = cell(numel(bigCourt),1);
countryDistance = cell(numel(bigCourt),1);
decisionDistance = cell(numel(bigCourt),1);
for j = 1:numel(bigCourt)
    ind = find(court==bigCourt(j));
    bench = judge(ind);
    toBench = append(baseURL,link(ind));
    %% Scrape relevant paragraph for each judge in the current big court
    judgeHtml = cell(numel(ind),1);
    keyPassage = strings(numel(ind),1);
    % The relevant paragraph always begins as follows:
    init = "The largest group of asylum seekers appearing before Judge";
    % ...and ends with:
    term = "</span";
    for k = 1:numel(ind)
        judgeHtml{k} = webread(toBench(k));
        foo = strfind(judgeHtml{k},init);
        if isscalar(foo)
            bar = strfind(judgeHtml{k},term);
            if isscalar(bar)
                keyPassage(k) = judgeHtml{k}(foo:bar);
            else
                warning("numel(bar) ~= 1");
                keyPassage(k) = "";
            end
        else
            warning("numel(foo) ~= 1");
            keyPassage(k) = "";
        end
    end
    %% Parse relevant paragraphs using TRAC's formulaic language
    % Some data is missing from TRAC so we have to use for loops etc.
    % Get top country
    foo = regexp(keyPassage,'came\sfrom\s[\w\s]+','match');
    nil = find(cellfun(@length,foo)==0);
    for k = 1:numel(nil)
        foo{nil(k)} = ""; 
    end
    topCountry = regexprep(string(foo),'came\sfrom\s','');
    % Get top country percentage
    foo = regexp(keyPassage,'country\smade\sup\s\d+\.\d','match');
    nil = find(cellfun(@length,foo)==0);
    for k = 1:numel(nil)
        foo{nil(k)} = ""; 
    end
    topPercentage = double(regexprep(string(foo),'country\smade\sup\s',''));
    % Get the rest
    foo = regexp(keyPassage,'were:\s.+\.<','match');
    nil = find(cellfun(@length,foo)==0);
    for k = 1:numel(nil)
        foo{nil(k)} = ""; 
    end
    bar = regexprep(string(foo),'\s+',' '); % regularize white space
    % We can't do an array in practice here, i.e.
        % split(replace(bar,["were: ",".<"],""),', ')
    % fails because of irregular rows. So, we have to use cells
    theRest = cell(numel(bar),1);
    %% Package the data
    country{j} = cell(numel(bar),1);
    percentage{j} = cell(numel(bar),1);
    for k = 1:numel(bar)
        theRest{k} = split(replace(bar(k),["were: ",".<"],""),', ');
        theRestCountry = regexprep(theRest{k},' \(\d+\.\d%\)','');
        theRestPercentage = ...
            double(replace(regexprep(theRest{k},'[a-zA-Z\s]+',''),["(","%)"],""));
        country{j}{k} = [topCountry(k);theRestCountry];
        percentage{j}{k} = [topPercentage(k);theRestPercentage];
    end
    %% Get all the countries before the court
    allCountriesBeforeCourt{j} = [];
    for k = 1:numel(country{j})
        allCountriesBeforeCourt{j} = unique([allCountriesBeforeCourt{j};country{j}{k}]);
    end
    %% Build distributions over countries for each judge
    % Distribute "other" equally amongst the non-represented entries of
    % allCountriesBeforeCourt{j} IAW the principle of indifference
    countryDistribution{j} = cell(size(country{j}));
    for k = 1:numel(country{j})
        countryDistribution{j}{k} = zeros(1,numel(allCountriesBeforeCourt{j}));
        for ell = 1:numel(country{j}{k})
            foo = find(ismember(allCountriesBeforeCourt{j},country{j}{k}(ell)));
            countryDistribution{j}{k}(foo) = percentage{j}{k}(ell)/100; %#ok<FNDSB>
        end
    end
    countryDistribution{j} = cell2mat(countryDistribution{j});
    foo = countryDistribution{j}==0;
    bar = (1-sum(countryDistribution{j},2))./sum(foo,2);
    % Make distribution{j} normalized with full support by filling blanks
    countryDistribution{j} = countryDistribution{j}+diag(bar)*foo;
    %% Build distributions over decisions for each judge
    decisionDistribution = [asylum(ind),other(ind),denied(ind)]/100;
    % Normalize to handle fixed point arithmetic in TRAC
    decisionDistribution = diag(sum(decisionDistribution,2))\decisionDistribution;
    %% NOW. COMPUTE DISTANCES BETWEEN JUDGES...
    % ...in country and decision spaces. Instances where a pair are close
    % in country space and far in decision space are presumptive instances
    % of process incoherence.
    %
    % Since half the L^1 distance between distributions equals the
    % 1-Wasserstein distance a la
    % https://en.wikipedia.org/wiki/Total_variation_distance_of_probability_measures#Connection_to_transportation_theory
    % that seems like a great choice here.
    countryDistance{j} = zeros(numel(ind));
    decisionDistance{j} = zeros(numel(ind));
    for k1 = 1:numel(ind)
        for k2 = 1:numel(ind)
            countryDistance{j}(k1,k2) = ...
                .5*sum(abs(countryDistribution{j}(k1,:)-countryDistribution{j}(k2,:)));
            decisionDistance{j}(k1,k2) = ...
                .5*sum(abs(decisionDistribution(k1,:)-decisionDistribution(k2,:)));
        end
    end
    %% Determine quantitative Pareto dominance
    obj = [countryDistance{j}(:).';1-decisionDistance{j}(:).'];
    dom = nan(size(obj,2),1);
    for k = 1:numel(dom)
        obj_k = obj(:,k)*ones(1,size(obj,2));
        dominator = min(obj_k-obj);
        dom(k) = max(dominator);
    end
    %% Identify the Pareto front per court
    [k1,k2] = find(triu(reshape(dom==0,[numel(ind),numel(ind)]),1));
    k1k2 = sortrows([k1,k2]);
    %% Plot pie charts for each point on the Pareto front
    for k = 1:size(k1k2,1)
        k1 = k1k2(k,1); 
        k2 = k1k2(k,2); 
        m1 = ind(k1); 
        m2 = ind(k2); 
        %%
        ind1 = countryDistribution{j}(k1,:)>min(countryDistribution{j}(k1,:));
        ind2 = countryDistribution{j}(k2,:)>min(countryDistribution{j}(k2,:));
        foo1 = countryDistribution{j}(k1,ind1);
        foo2 = countryDistribution{j}(k2,ind2);
        bar1 = [foo1,1-sum(foo1)];
        bar2 = [foo2,1-sum(foo2)];
        try
            figure('Position',[0,0,560,210]);
            subplot(1,5,1:3);
                labels1 = [allCountriesBeforeCourt{j}(ind1);"Other"];
                labels2 = [allCountriesBeforeCourt{j}(ind2);"Other"];
                labels12 = unique([labels1;labels2]);
                data1 = zeros(length(labels12),1);
                data2 = zeros(length(labels12),1);
                for i = 1:length(labels12)
                    if any(strcmp(labels12{i},labels1))
                        data1(i) = bar1(strcmp(labels1,labels12{i}));
                    end
                    if any(strcmp(labels12{i},labels2))
                        data2(i) = bar2(strcmp(labels2,labels12{i}));
                    end
                end            
                bh = barh([100*data1,100*data2]);
                bh(1).FaceColor = .75*[1,1,1];
                bh(2).FaceColor = .5*[1,1,1];
                set(gca,'yticklabel',labels12);
                title(join([string(bigCourt(j)),"court caseload percentages"]));
                legend(judge(m1),judge(m2),'Location','best');
            subplot(1,5,4);
                tmp = [0,cumsum(decisionDistribution(k1,:))];
                hold on;
                fooDenied = plot(-1,-1,'color',colorDenied,'LineWidth',6);
                fooOther = plot(-1,-1,'color',colorOther,'LineWidth',6);
                fooAsylum = plot(-1,-1,'color',colorGranted,'LineWidth',6);
                legend([fooDenied,fooOther,fooAsylum],...
                    {'denied','other','granted'},...
                    'Location','best','AutoUpdate','off');%,'Interpreter','latex');
                p = patch([0,1,1,0],100*tmp([1,1,2,2]),colorGranted);
                p = patch([0,1,1,0],100*tmp([2,2,3,3]),colorOther);
                p = patch([0,1,1,0],100*tmp([3,3,4,4]),colorDenied);
                set(gca,'Ytick',[],'XTick',[]);
                axis([0,1,0,100]);
                ylabel("proportion of asylum decisions");
                title(strtok(judge(m1),','));
            subplot(1,5,5);
                tmp = [0,cumsum(decisionDistribution(k2,:))];
                hold on;
                fooDenied = plot(-1,-1,'color',colorDenied,'LineWidth',6);
                fooOther = plot(-1,-1,'color',colorOther,'LineWidth',6);
                fooAsylum = plot(-1,-1,'color',colorGranted,'LineWidth',6);
                legend([fooDenied,fooOther,fooAsylum],...
                    {'denied','other','granted'},...
                    'Location','best','AutoUpdate','off');%,'Interpreter','latex');
                p = patch([0,1,1,0],100*tmp([1,1,2,2]),colorGranted);
                p = patch([0,1,1,0],100*tmp([2,2,3,3]),colorOther);
                p = patch([0,1,1,0],100*tmp([3,3,4,4]),colorDenied);
                set(gca,'Ytick',[0,100],'XTick',[]);
                axis([0,1,0,100]);
                % ylabel("proportion of asylum decisions");
                title(strtok(judge(m2),','));
            %
            fileName = join(["Court",strrep(string(bigCourt(j))," ","_"),...
                strtok(judge(m1),','),strtok(judge(m2),','),".png"],"");
            print(fileName,'-r600','-dpng');
        catch
        end
    end
end
